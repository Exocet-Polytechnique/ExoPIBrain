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
    sensors: HashMap<TemperatureSensorName, TemperatureSensor>,
    current_sensor: TemperatureSensorName,
}

#[derive(Clone, Copy, Deserialize, Debug, Hash, PartialEq, Eq)]
pub enum TemperatureSensorName {
    H2Plate = 0,
    Batteries = 1,
    FuelCellControllers = 2,
    H2Tanks = 3,
    Extra = 4,
}

struct TemperatureSensor {
    pub path: PathBuf,
    pub max: f32,
    pub alert: f32,
    pub warning: f32,
}

fn check_temperature(sensor: &TemperatureSensor, value: f32) -> Option<Exception> {
    if value > sensor.max {
        Some(Exception::CriticalTemperature)
    } else if value > sensor.alert {
        Some(Exception::AlertTemperature)
    } else if value > sensor.warning {
        Some(Exception::WarningTemperature)
    } else {
        None
    }
}

fn read_sensor(sensor_path: &PathBuf) -> Result<f32, Exception> {
    if !sensor_path.is_file() {
        return Err(Exception::InfoNotConnected);
    }
    let mut file = File::open(sensor_path)?;
    let mut file_content = String::new();
    file.read_to_string(&mut file_content)?;

    let mut lines = file_content.lines().map(|x| x.trim());
    if !lines.next().ok_or(Exception::InfoBadData)?.ends_with("YES") {
        return Err(Exception::InfoBadData);
    }

    let value_line = lines.next().ok_or(Exception::InfoBadData)?;
    let value_position = value_line.find("t=").ok_or(Exception::InfoBadData)?;
    let value = value_line[value_position + 2..].parse::<f32>()? / 1000.0;

    Ok(value)
}

impl Sensor for Temperature {
    type Config = Vec<TemperatureConfig>;

    fn new(config: &Self::Config) -> Self {
        let sensors = config
            .iter()
            .map(|x| {
                (
                    x.name,
                    TemperatureSensor {
                        max: x.max,
                        alert: x.alert,
                        warning: x.warn,
                        path: PathBuf::from(format!(
                            "/sys/bus/w1/devices/28-{:012x}/w1_slave",
                            x.address
                        )),
                    },
                )
            })
            .collect();

        Temperature {
            sensors,
            current_sensor: TemperatureSensorName::H2Plate,
        }
    }

    fn read(&mut self) -> (SensorData, Option<Exception>) {
        self.current_sensor = match self.current_sensor {
            TemperatureSensorName::H2Plate => TemperatureSensorName::Batteries,
            TemperatureSensorName::Batteries => TemperatureSensorName::FuelCellControllers,
            TemperatureSensorName::FuelCellControllers => TemperatureSensorName::H2Tanks,
            TemperatureSensorName::H2Tanks => TemperatureSensorName::Extra,
            TemperatureSensorName::Extra => TemperatureSensorName::H2Plate,
        };

        let sensor = &self.sensors[&self.current_sensor];

        match read_sensor(&sensor.path) {
            Ok(data) => (
                SensorData::Temperature((self.current_sensor, Some(data))),
                check_temperature(sensor, data),
            ),
            Err(exception) => (
                SensorData::Temperature((self.current_sensor, None)),
                Some(exception),
            ),
        }
    }
}
