use super::{
    common::{sensor::Sensor, sensor_data::SensorData, serial_device::SerialDevice},
    Exception,
};
use crate::config::GpsConfig;

pub struct Gps {
    serial: SerialDevice,
}

const READ_TIMEOUT: f32 = 1.0;

#[derive(Debug, Clone, Copy)]
pub struct GpsData {
    pub nmea_time: Option<f32>,
    pub speed_knots: Option<f32>,
    pub course_angle: Option<f32>,
    pub latitude_deg: Option<f32>,
    pub longitude_deg: Option<f32>,
}

fn to_degrees(sensor_value: f32) -> f32 {
    let decimal_value = sensor_value / 100.0;
    let degrees = f32::floor(decimal_value);
    let mm_mmmm = (decimal_value - degrees) / 0.6;

    degrees + mm_mmmm
}

impl Gps {
    fn try_read(&self) -> Result<SensorData, Exception> {
        let mut data_line = String::new(); // self.serial.readln();
        while !data_line.contains("$GPRMC") {
            data_line = self.serial.readln(READ_TIMEOUT)?;
        }

        let split_data: Vec<&str> = data_line.split(',').collect();

        Ok(SensorData::Gps(Some(GpsData {
            nmea_time: split_data[1].parse().ok(),
            speed_knots: split_data[7].parse().ok(),
            course_angle: split_data[8].parse().ok(),
            latitude_deg: split_data[3].parse().ok().map(|x| to_degrees(x)),
            longitude_deg: split_data[5].parse().ok().map(|x| to_degrees(x) * -1.0),
        })))
    }
}

impl Sensor for Gps {
    type Config = GpsConfig;

    fn new(config: &Self::Config) -> Self {
        Self {
            serial: SerialDevice::initialize(&config.serial),
        }
    }

    fn read(&mut self) -> (SensorData, Option<Exception>) {
        match self.try_read() {
            Ok(d) => (d, None),
            Err(e) => (SensorData::Gps(None), Some(e)),
        }
    }
}
