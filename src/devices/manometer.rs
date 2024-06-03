use std::sync::{Arc, Mutex};

use rppal::spi::Spi;

use super::{
    common::{sensor::Sensor, sensor_data::SensorData},
    Exception,
};
use crate::config::ManometerConfig;

pub struct Manometer {
    spi_device: Arc<Mutex<Spi>>,
}

impl Sensor for Manometer {
    type Config = (Arc<Mutex<Spi>>, ManometerConfig);

    fn new(config: &Self::Config) -> Self {
        Manometer {
            spi_device: config.0.clone(),
        }
    }

    fn read(&mut self) -> (SensorData, Option<Exception>) {
        let out_data: [u8; 2] = [3, 1];
        let mut in_data: [u8; 2] = [0; 2];

        let size_result = self
            .spi_device
            .lock()
            .unwrap()
            .transfer(&mut in_data, &out_data);

        todo!()
    }
}
