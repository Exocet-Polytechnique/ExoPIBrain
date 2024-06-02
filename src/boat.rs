use std::{
    sync::{
        mpsc::{self, Receiver},
        Arc, RwLock,
    },
    time::Instant,
};

use crate::{
    config::load_config,
    devices::{
        common::{
            message::Message,
            sensor_data::SensorData,
            sensor_thread::{SensorThread, ThreadMessaging},
        },
        gps::GpsDevice,
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

    /// Devices
    gps_thread: SensorThread<GpsDevice>,
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

        let telemetry = Telemetry::new(&config.telemetry);

        Boat {
            data_receiver,
            error_receiver,
            telemetry,
            last_telemetry_time: Instant::now(),
            telemetry_send_interval: config.telemetry.send_interval,
            telemetry_data: TelemetryData::new(),
            gps_thread: SensorThread::new(messaging, &config.gps, crate::devices::Name::Gps),
            stop_signal,
        }
    }

    fn start(&mut self) {
        self.gps_thread.start();
    }

    fn shutdown(&mut self) {
        *self.stop_signal.write().unwrap() = true;
    }

    fn update_data(data: &SensorData, telemetry: &mut TelemetryData) {
        match data {
            SensorData::Gps(d) => telemetry.gps = *d,
            _ => (),
        }
    }

    fn running_loop(&mut self) -> () {
        let mut TEMP_COUNTER = 0;

        loop {
            for error in self.error_receiver.try_iter() {
                // self.interface.dispatch_message(error);
                if (error.get_exception() as u16) < 0x30 {
                    break;
                }
            }

            for data in self.data_receiver.try_iter() {
                Self::update_data(&data, &mut self.telemetry_data);
            }

            if self.last_telemetry_time.elapsed().as_secs_f32() >= self.telemetry_send_interval {
                TEMP_COUNTER += 1;
                self.telemetry.send(&self.telemetry_data);
                self.last_telemetry_time = Instant::now();
            }

            if TEMP_COUNTER > 15 {
                break;
            }

            // self.interface.render();
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
