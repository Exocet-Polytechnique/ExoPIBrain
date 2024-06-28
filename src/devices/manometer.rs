use std::sync::{Arc, Mutex};

use rppal::spi::Spi;

use super::{
    common::{sensor::Sensor, sensor_data::SensorData},
    Exception,
};
use crate::config::ManometerConfig;

const MAX_ADC_VALUE: f32 = 0x3F as f32;
const ADC_BIAS: f32 = 1.038;

pub enum ManometerName {
    HighPressure,
    LowPressure,
}

pub struct Manometer {
    spi_device: Arc<Mutex<Spi>>,
    channel: u8,
    max_bar: f32,
    name: ManometerName,
}

impl Manometer {
    fn read_adc(&mut self) -> Result<f32, Exception> {
        let config_byte = 0x80 | (self.channel << 4);
        let out_data: [u8; 3] = [1, config_byte, 0];
        let mut in_data: [u8; 3] = [0xFF; 3];

        let size_result = self
            .spi_device
            .lock()
            .unwrap()
            .transfer(&mut in_data, &out_data)?;

        if size_result != 3 {
            return Err(Exception::InfoBadData);
        }

        if (in_data[1] >> 3) != 0 {
            return Err(Exception::InfoBadData);
        }

        let value_u16 = (((in_data[1] & 0x03) as u16) << 8) | (in_data[2] as u16);

        Ok((((value_u16 as f32) / MAX_ADC_VALUE) * self.max_bar) * ADC_BIAS)
    }
}

impl Sensor for Manometer {
    type Config = (Arc<Mutex<Spi>>, ManometerConfig, ManometerName);

    fn new(config: &Self::Config) -> Self {
        Manometer {
            spi_device: config.0.clone(),
            channel: config.1.channel,
            max_bar: config.1.max_bar,
            name: config.2,
        }
    }

    fn read(&mut self) -> (SensorData, Option<Exception>) {
        let value = self.read_adc();

        let data = match self.name {
            ManometerName::LowPressure => SensorData::LowPressureManometer(value.ok()),
            ManometerName::HighPressure => SensorData::HighPressureManometer(value.ok()),
        };

        (data, value.err())
    }
}
