// use exo_pi_brain_rs::{devices::SensorData, interface::Interface};

use std::time::Duration;

use exo_pi_brain_rs::{
    config::{GpsConfig, SerialConfig},
    devices::gps::GpsDevice,
};

fn main() {
    // let mut interface = Interface::new();
    // loop {
    //     let should_close = interface.update(&SensorData {
    //         fuel_cell_a: None,
    //         fuel_cell_b: None,
    //     });
    //     if should_close {
    //         break;
    //     }
    //     interface.render();
    // }
    let mut gps_dev = GpsDevice::initialize(&GpsConfig {
        priority: 2,
        read_interval: 1.0,
        serial: SerialConfig {
            baudrate: 9600,
            port: "/dev/serial0".to_string(),
        },
    });

    loop {
        let data = gps_dev.read().unwrap();
        println!("{data:?}");
        std::thread::sleep(Duration::from_secs(1));
    }
}
