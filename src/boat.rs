use std::{
    sync::{
        mpsc::{self, Receiver},
        Arc, Mutex, RwLock,
    },
    thread::sleep,
    time::{Duration, Instant},
};

use rppal::{gpio::Gpio, i2c::I2c, spi::Spi};

use crate::{
    config::load_config,
    devices::{
        actuator::Actuator,
        battery::BatteryGauge,
        button::Button,
        common::{
            message::Message,
            sensor_data::SensorData,
            sensor_thread::{SensorThread, ThreadMessaging},
        },
        contactor::Contactor,
        fuel_cell::{FuelCell, FuelCellName},
        gps::Gps,
        manometer::{Manometer, ManometerName},
        temperature::{Temperature, TemperatureSensorName},
        Exception, Name,
    },
    interface::{Interface, InterfaceData},
    procedures::{
        shutdown::BoatStopper,
        startup::{BoatStarter, StartupData},
    },
    telemetry::{Telemetry, TelemetryData},
};

pub struct Boat {
    data_receiver: Receiver<SensorData>,
    error_receiver: Receiver<Message>,
    stop_signal: Arc<RwLock<bool>>,

    telemetry: Telemetry,
    last_telemetry_time: Instant,
    telemetry_send_interval: f32,
    telemetry_data: TelemetryData,

    interface: Interface,
    interface_data: InterfaceData,
    last_interface_time: Instant,

    /// Procedures
    starter: BoatStarter,
    startup_data: Arc<RwLock<StartupData>>,
    stopper: BoatStopper,
    state: State,

    /// Devices (no IMU)
    gps_thread: SensorThread<Gps>,
    temperature_thread: SensorThread<Temperature>,
    battery_thread: SensorThread<BatteryGauge>,

    low_pressure_thread: SensorThread<Manometer>,
    high_pressure_thread: SensorThread<Manometer>,
    mv01_actuator: Arc<Mutex<Actuator>>,
    mv02_actuator: Arc<Mutex<Actuator>>,

    start_button: Button,
    stop_button: Button,
    dms: Arc<Mutex<Button>>,

    fuel_cell_a: SensorThread<FuelCell>,
    fuel_cell_b: SensorThread<FuelCell>,

    fca_relay: Arc<Mutex<Contactor>>,
    fcb_relay: Arc<Mutex<Contactor>>,
    source_isolation_contactor: Arc<Mutex<Contactor>>,
    level2_charge_contactor: Arc<Mutex<Contactor>>,
}

#[derive(PartialEq, Eq)]
enum State {
    Idle,
    Starting,
    Running,
    Stopping,
}

impl Boat {
    pub fn new() -> Boat {
        let config = load_config("device_config.toml");

        let (data_sender, data_receiver) = mpsc::channel();
        let (error_sender, error_receiver) = mpsc::channel();
        let stop_signal = Arc::new(RwLock::new(false));

        let messaging = ThreadMessaging {
            data_sender,
            error_sender: error_sender.clone(),
            stop_signal: stop_signal.clone(),
        };

        let spi_bus = Arc::new(Mutex::new(
            Spi::new(
                rppal::spi::Bus::Spi0,
                rppal::spi::SlaveSelect::Ss0,
                3_600_000,
                rppal::spi::Mode::Mode0,
            )
            .unwrap(),
        ));

        let i2c_bus = Arc::new(Mutex::new(I2c::new().unwrap()));

        let gpio = Gpio::new().unwrap();

        let mut fuel_cell_a = SensorThread::new(
            messaging.clone(),
            &(config.fuel_cell_a, FuelCellName::A),
            crate::devices::Name::FuelCellA,
        );
        let mut fuel_cell_b = SensorThread::new(
            messaging.clone(),
            &(config.fuel_cell_b, FuelCellName::B),
            crate::devices::Name::FuelCellB,
        );

        let fca_relay = Arc::new(Mutex::new(Contactor::initialize(&gpio, &config.fca_relay)));
        let fcb_relay = Arc::new(Mutex::new(Contactor::initialize(&gpio, &config.fcb_relay)));
        let source_isolation_contactor = Arc::new(Mutex::new(Contactor::initialize(
            &gpio,
            &config.source_isolation_contactor,
        )));
        let level2_charge_contactor = Arc::new(Mutex::new(Contactor::initialize(
            &gpio,
            &config.level2_charge_contactor,
        )));

        let dms = Arc::new(Mutex::new(Button::new(&gpio, &config.dms)));

        let mv01_actuator = Arc::new(Mutex::new(Actuator::initialize(&gpio, &config.valve1)));
        let mv02_actuator = Arc::new(Mutex::new(Actuator::initialize(&gpio, &config.valve2)));

        let startup_data = Arc::new(RwLock::new(StartupData::default()));
        let starter = BoatStarter::new(
            error_sender.clone(),
            startup_data.clone(),
            fuel_cell_a.get_sensor(),
            fuel_cell_b.get_sensor(),
            fca_relay.clone(),
            fcb_relay.clone(),
            mv01_actuator.clone(),
            mv02_actuator.clone(),
            source_isolation_contactor.clone(),
            level2_charge_contactor.clone(),
            dms.clone(),
        );

        let stopper = BoatStopper::new(
            error_sender.clone(),
            fuel_cell_a.get_sensor(),
            fuel_cell_b.get_sensor(),
            fca_relay.clone(),
            fcb_relay.clone(),
            mv01_actuator.clone(),
            mv02_actuator.clone(),
            source_isolation_contactor.clone(),
            level2_charge_contactor.clone(),
        );

        Boat {
            data_receiver,
            error_receiver,
            stop_signal,

            telemetry: Telemetry::new(&config.telemetry),
            last_telemetry_time: Instant::now(),
            telemetry_send_interval: config.telemetry.send_interval,
            telemetry_data: TelemetryData::new(),

            interface: Interface::new(),
            interface_data: InterfaceData::new(),
            last_interface_time: Instant::now(),

            state: State::Idle,
            startup_data,
            starter,
            stopper,

            gps_thread: SensorThread::new(
                messaging.clone(),
                &config.gps,
                crate::devices::Name::Gps,
            ),
            temperature_thread: SensorThread::new(
                messaging.clone(),
                &config.temperatures,
                crate::devices::Name::Temperatures,
            ),
            battery_thread: SensorThread::new(
                messaging.clone(),
                &(i2c_bus.clone(), config.battery_gauge),
                crate::devices::Name::BatteryGauge,
            ),

            low_pressure_thread: SensorThread::new(
                messaging.clone(),
                &(
                    spi_bus.clone(),
                    config.low_pressure_manometer,
                    ManometerName::LowPressure,
                ),
                crate::devices::Name::LowPressureManometer,
            ),
            high_pressure_thread: SensorThread::new(
                messaging.clone(),
                &(
                    spi_bus.clone(),
                    config.high_pressure_manometer,
                    ManometerName::HighPressure,
                ),
                crate::devices::Name::HighPressureManometer,
            ),
            mv01_actuator,
            mv02_actuator,

            start_button: Button::new(&gpio, &config.start_button),
            stop_button: Button::new(&gpio, &config.stop_button),
            dms,

            fuel_cell_a,
            fuel_cell_b,

            fca_relay,
            fcb_relay,
            source_isolation_contactor,
            level2_charge_contactor,
        }
    }

    fn update_data(&mut self) {
        for data in self.data_receiver.try_iter() {
            match data {
                SensorData::Gps(values) => {
                    self.telemetry_data.gps = values;
                    self.interface_data.speed = match values {
                        Some(x) => x.speed_knots.map(|speed| speed * 1.852),
                        None => None,
                    }
                }
                SensorData::Temperature((name, value)) => {
                    self.telemetry_data.temperature.insert(name, value);
                    match name {
                        TemperatureSensorName::H2Plate => {
                            self.interface_data.h2_plate_temperature = value
                        }
                        TemperatureSensorName::Batteries => {
                            self.interface_data.battery_temperature = value
                        }
                        TemperatureSensorName::FuelCellControllers => {
                            self.interface_data.fuel_cell_controllers_temperature = value
                        }
                        TemperatureSensorName::H2Tanks => {
                            self.interface_data.h2_tanks_temperature = value;
                            self.startup_data.write().unwrap().h2_plate_temperature = value;
                        }
                    }
                }
                SensorData::FuelCellA(values) => {
                    self.telemetry_data.fuel_cell_a = values;

                    self.interface_data.fuel_cell_a_temperature =
                        values.and_then(|x| x.temperature);
                }
                SensorData::FuelCellB(values) => {
                    self.telemetry_data.fuel_cell_b = values;

                    self.interface_data.fuel_cell_b_temperature =
                        values.and_then(|x| x.temperature);
                }
                SensorData::Batteries(values) => {
                    self.telemetry_data.battery = values;

                    self.interface_data.battery_capacity = values.map(|x| x.charge_level);
                    self.interface_data.battery_voltage = values.map(|x| x.voltage);
                    self.interface_data.battery_current = values.map(|x| x.current);
                }
                SensorData::HighPressureManometer(value) => {
                    self.interface_data.high_pressure = value;
                    self.startup_data.write().unwrap().high_pressure = value;
                }
                SensorData::LowPressureManometer(value) => {
                    self.interface_data.low_pressure = value;
                    self.startup_data.write().unwrap().low_pressure = value;
                }
                _ => (),
            };
        }
    }

    fn run(&mut self) -> () {
        loop {
            match self.state {
                State::Idle => {
                    if self.start_button.read() {
                        self.state = State::Starting;
                        self.starter.start();
                    } else if self.stop_button.read() {
                        break;
                    }
                }
                State::Running => {
                    if self.dms.lock().unwrap().read() {
                        self.state = State::Stopping;
                        self.stopper.stop();
                    } else if self.stop_button.read() {
                        self.state = State::Stopping;
                        self.stopper.stop();
                    }
                }
                _ => (),
            }

            for error in self.error_receiver.try_iter() {
                self.interface.dispatch_message(error.clone());
                if self.state == State::Running && error.is_critical() {
                    self.state = State::Stopping;
                    self.stopper.stop();
                }

                if error.get_name() == Name::System {
                    match error.get_exception() {
                        Exception::InfoStartupSuccess => {
                            if self.state == State::Starting {
                                self.state = State::Running;
                            }
                        }
                        Exception::InfoStartupFailed => {
                            if self.state == State::Starting {
                                self.state = State::Stopping;
                            }
                        }
                        Exception::InfoShutdownFailed => {
                            break;
                        }
                        Exception::InfoShutdownSuccess => {
                            if self.state == State::Stopping {
                                self.state = State::Idle;
                            }
                        }
                        _ => (),
                    }
                }
            }

            self.update_data();

            if self.last_telemetry_time.elapsed().as_secs_f32() >= self.telemetry_send_interval {
                self.telemetry.send(&self.telemetry_data);
                self.last_telemetry_time = Instant::now();
            }

            if self.last_interface_time.elapsed().as_secs_f32() >= 1.0 {
                self.interface.render(&self.interface_data);
                self.last_interface_time = Instant::now();
            }

            if self.interface.should_quit() {
                break;
            }

            std::thread::sleep(Duration::from_millis(50));
        }

        *self.stop_signal.write().unwrap() = true;

        while !(self.gps_thread.is_stopped()
            && self.temperature_thread.is_stopped()
            && self.battery_thread.is_stopped()
            && self.low_pressure_thread.is_stopped()
            && self.high_pressure_thread.is_stopped()
            && self.fuel_cell_a.is_stopped()
            && self.fuel_cell_b.is_stopped())
        {
            sleep(Duration::from_millis(100));
        }
    }
}
