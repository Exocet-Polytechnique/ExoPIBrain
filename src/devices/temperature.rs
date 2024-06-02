use std::{collections::HashMap, fs::File, io::Read, path::PathBuf};

use serde::Deserialize;

use crate::config::TemperatureConfig;

use super::{
    common::{sensor::Sensor, sensor_data::SensorData},
    Exception,
};

pub type TemperatureData = HashMap<TemperatureSensorName, Option<f32>>;

/// For the temperature sensors to work, the following line must be added to `/boot/config.txt`:
/// ```
/// dtoverlay=w1-gpio
/// ```
/// By default, the raspberry pi uses GPIO4 for the w1 interface, so the temperatures sensors
/// should be connected there
/// Also, the following two lines must be added to `/etc/modules`:
/// ```
/// w1-gpio
/// w1-therm
/// ```
pub struct Temperature {
    // h2_plate_path: PathBuf,
    // batteries_path: PathBuf,
    // fuel_cell_controllers_path: PathBuf,
    // h2_tanks_path: PathBuf,
    // extra_path: PathBuf,
    current_sensor_index: u8,
}

#[derive(Deserialize, Debug, Hash, PartialEq, Eq)]
pub enum TemperatureSensorName {
    H2Plate,
    Batteries,
    FuelCellControllers,
    H2Tanks,
    Extra,
}

fn check_temperature(name: TemperatureSensorName, value: f32) -> bool {
    true
}

impl Temperature {
    fn read_sensor(&self, sensor_path: &PathBuf) -> Option<f32> {
        if !sensor_path.is_file() {
            return None;
        }
        let mut file = File::open(sensor_path).ok()?;
        let mut file_content = String::new();
        file.read_to_string(&mut file_content).ok()?;

        let mut lines = file_content.lines().map(|x| x.trim());
        if !lines.next()?.ends_with("YES") {
            return None;
        }

        let value_line = lines.next()?;
        let value_position = value_line.find("t=")?;
        let value = value_line[value_position + 2..].parse::<f32>().ok()? / 1000.0;

        Some(value)
    }
}

impl Sensor for Temperature {
    type Config = Vec<TemperatureConfig>;

    fn new(config: &Self::Config) -> Self {
        // use maps and clean this code up
        Temperature {
            // h2_plate_path: PathBuf::from(format!(
            //     "/sys/bus/w1/devices/28-{:012x}/w1_slave",
            //     config.h2_plate.address
            // )),
            // batteries_path: PathBuf::from(format!(
            //     "/sys/bus/w1/devices/28-{:012x}/w1_slave",
            //     config.batteries.address
            // )),
            // fuel_cell_controllers_path: PathBuf::from(format!(
            //     "/sys/bus/w1/devices/28-{:012x}/w1_slave",
            //     config.fuel_cell_controllers.address
            // )),
            // h2_tanks_path: PathBuf::from(format!(
            //     "/sys/bus/w1/devices/28-{:012x}/w1_slave",
            //     config.h2_tanks.address
            // )),
            // extra_path: PathBuf::from(format!(
            //     "/sys/bus/w1/devices/28-{:012x}/w1_slave",
            //     config.extra.address
            // )),
            current_sensor_index: 0,
        }
    }

    fn read(&mut self) -> (SensorData, Option<Exception>) {
        // let data = match self.current_sensor_index {
        //     0 => SensorData::H2PlateTemperature(self.read_sensor(&self.h2_plate_path)),
        //     1 => self.current_data.batteries = self.read_sensor(&self.batteries_path),
        //     2 => {
        //         self.current_data.fuel_cell_controllers =
        //             self.read_sensor(&self.fuel_cell_controllers_path)
        //     }
        //     3 => self.current_data.h2_tanks = self.read_sensor(&self.h2_tanks_path),
        //     4 => self.current_data.extra = self.read_sensor(&self.extra_path),
        //     _ => panic!("Temperature sensor index should not be > 4."),
        // };
        //
        // self.current_sensor_index += 1;
        // if self.current_sensor_index > 4 {
        //     self.current_sensor_index = 0;
        // }

        (
            SensorData::Temperature((TemperatureSensorName::H2Plate, None)),
            None,
        )
    }
}
