use super::common::{exceptions::DeviceException, serial_device::SerialDevice};
use crate::config::GpsConfig;

pub struct GpsDevice {
    serial: SerialDevice,
    read_timeout: f32,
}

#[derive(Debug)]
pub struct GpsData {
    nmea_time: Option<f32>,
    speed_knots: Option<f32>,
    course_angle: Option<f32>,
    latitude_deg: Option<f32>,
    longitude_deg: Option<f32>,
}

fn to_degrees(sensor_value: f32) -> f32 {
    let decimal_value = sensor_value / 100.0;
    let degrees = f32::floor(decimal_value);
    let mm_mmmm = (decimal_value - degrees) / 0.6;

    degrees + mm_mmmm
}

impl GpsDevice {
    pub fn initialize(config: &GpsConfig) -> GpsDevice {
        GpsDevice {
            serial: SerialDevice::initialize(&config.serial),
            read_timeout: config.read_interval,
        }
    }

    pub fn read(&mut self) -> Result<GpsData, DeviceException> {
        let mut data_line = String::new(); // self.serial.readln();
        while !data_line.contains("$GPRMC") {
            data_line = self.serial.readln(self.read_timeout)?;
        }

        let split_data: Vec<&str> = data_line.split(',').collect();

        Ok(GpsData {
            nmea_time: split_data[1].parse().ok(),
            speed_knots: split_data[7].parse().ok(),
            course_angle: split_data[8].parse().ok(),
            latitude_deg: split_data[3].parse().ok().map(|x| to_degrees(x)),
            longitude_deg: split_data[5].parse().ok().map(|x| to_degrees(x) * -1.0),
        })
    }
}
