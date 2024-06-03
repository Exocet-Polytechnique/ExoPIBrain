use std::{
    sync::{
        mpsc::{self, Receiver},
        Arc, Mutex, RwLock,
    },
    thread,
    time::{Duration, Instant},
};

use rppal::spi::Spi;

use crate::{
    config::load_config,
    devices::{
        common::{
            message::Message,
            sensor_data::SensorData,
            sensor_thread::{SensorThread, ThreadMessaging},
        },
        gps::Gps,
        manometer::Manometer,
        temperature::{Temperature, TemperatureSensorName},
    },
    interface::{Interface, InterfaceData},
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

    /// Devices
    gps_thread: SensorThread<Gps>,
    temperature_thread: SensorThread<Temperature>,
    low_pressure_thread: SensorThread<Manometer>,
    high_pressure_thread: SensorThread<Manometer>,
}

impl Boat {
    pub fn new() -> Boat {
        let config = load_config("device_config.toml");

        let (data_sender, data_receiver) = mpsc::channel();
        let (error_sender, error_receiver) = mpsc::channel();
        let stop_signal = Arc::new(RwLock::new(false));

        let messaging = ThreadMessaging {
            data_sender,
            error_sender,
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

        let telemetry = Telemetry::new(&config.telemetry);

        Boat {
            data_receiver,
            error_receiver,
            telemetry,
            last_telemetry_time: Instant::now(),
            telemetry_send_interval: config.telemetry.send_interval,
            telemetry_data: TelemetryData::new(),
            interface: Interface::new(),
            interface_data: InterfaceData::new(),
            last_interface_time: Instant::now(),
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
            low_pressure_thread: SensorThread::new(
                messaging.clone(),
                &(spi_bus.clone(), config.low_pressure_manometer),
                crate::devices::Name::LowPressureManometer,
            ),
            high_pressure_thread: SensorThread::new(
                messaging.clone(),
                &(spi_bus.clone(), config.high_pressure_manometer),
                crate::devices::Name::HighPressureManometer,
            ),
            stop_signal,
        }
    }

    fn start(&mut self) {
        self.gps_thread.start();
        self.temperature_thread.start();
    }

    fn shutdown(&mut self) {
        *self.stop_signal.write().unwrap() = true;

        while !(self.gps_thread.is_stopped() && self.temperature_thread.is_stopped()) {}
    }

    fn update_data(
        data: &SensorData,
        telemetry: &mut TelemetryData,
        interface: &mut InterfaceData,
    ) {
        match data {
            SensorData::Gps(values) => {
                telemetry.gps = *values;
                interface.speed = match *values {
                    Some(x) => x.speed_knots.map(|speed| speed * 1.852),
                    None => None,
                }
            }
            SensorData::Temperature((name, value)) => {
                telemetry.temperature.insert(*name, *value);
                match name {
                    TemperatureSensorName::H2Plate => interface.h2_plate_temperature = *value,
                    TemperatureSensorName::Batteries => interface.battery_temperature = *value,
                    TemperatureSensorName::FuelCellControllers => {
                        interface.fuel_cell_controllers_temperature = *value
                    }
                    TemperatureSensorName::H2Tanks => interface.h2_tanks_temperature = *value,
                }
            }
            _ => (),
        };
    }

    fn running_loop(&mut self) -> () {
        loop {
            for error in self.error_receiver.try_iter() {
                self.interface.dispatch_message(&error);
                if (error.get_exception() as u16) < 0x30 {
                    break;
                }
            }

            for data in self.data_receiver.try_iter() {
                Self::update_data(&data, &mut self.telemetry_data, &mut self.interface_data);
            }

            if self.last_telemetry_time.elapsed().as_secs_f32() >= self.telemetry_send_interval {
                // self.telemetry.send(&self.telemetry_data);
                self.last_telemetry_time = Instant::now();
            }

            if self.last_interface_time.elapsed().as_secs_f32() >= 10.0 {
                self.interface.render(&self.interface_data);
                self.last_interface_time = Instant::now();
            }

            if self.interface.should_quit(20) {
                break;
            }
            thread::sleep(Duration::from_millis(500));
        }
    }

    // pub fn run(&mut self) -> ! {
    pub fn run(&mut self) -> () {
        // loop {
        self.start();
        self.running_loop();
        self.shutdown();
        // }
    }
}
