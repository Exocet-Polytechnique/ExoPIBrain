use std::{
    sync::{mpsc, Arc, RwLock},
    thread,
    time::{Duration, Instant},
};

use exo_pi_brain_rs::{
    config::load_config,
    devices::{
        common::sensor_thread::{SensorThread, ThreadMessaging},
        gps::GpsDevice,
    },
};

fn main() {
    let (txd, rxd) = mpsc::channel();
    let (txe, _rxe) = mpsc::channel();
    let stop_signal = Arc::new(RwLock::new(false));

    let messaging = ThreadMessaging {
        data_sender: txd,
        error_sender: txe,
        stop_signal: stop_signal.clone(),
    };

    let config = load_config("device_config.toml");

    let mut sensor_thread: SensorThread<GpsDevice> = SensorThread::new(messaging, &config.gps);

    sensor_thread.start();

    let start = Instant::now();

    while start.elapsed().as_secs() < 5 {
        for data in rxd.try_iter() {
            println!("{:?}", data);
        }
        thread::sleep(Duration::from_millis(500));
    }

    *stop_signal.write().unwrap() = true;
}
