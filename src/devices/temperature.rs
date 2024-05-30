use std::{fs::File, io::Read, path::PathBuf};

use crate::config::TemperatureSensorsConfig;

#[derive(Debug, Clone, Copy)]
pub struct TemperatureData {
    pub h2_plate: Option<f32>,
    pub batteries: Option<f32>,
    pub fuel_cell_controllers: Option<f32>,
    pub h2_tanks: Option<f32>,
    pub extra: Option<f32>,
}

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
    h2_plate_path: PathBuf,
    batteries_path: PathBuf,
    fuel_cell_controllers_path: PathBuf,
    h2_tanks_path: PathBuf,
    extra_path: PathBuf,
    current_sensor_index: u8,
    current_data: TemperatureData,
}

impl Temperature {
    pub fn initialize(config: &TemperatureSensorsConfig) -> Temperature {
        Temperature {
            h2_plate_path: PathBuf::from(format!(
                "/sys/bus/w1/devices/28-{:012x}/w1_slave",
                config.h2_plate.address
            )),
            batteries_path: PathBuf::from(format!(
                "/sys/bus/w1/devices/28-{:012x}/w1_slave",
                config.batteries.address
            )),
            fuel_cell_controllers_path: PathBuf::from(format!(
                "/sys/bus/w1/devices/28-{:012x}/w1_slave",
                config.fuel_cell_controllers.address
            )),
            h2_tanks_path: PathBuf::from(format!(
                "/sys/bus/w1/devices/28-{:012x}/w1_slave",
                config.h2_tanks.address
            )),
            extra_path: PathBuf::from(format!(
                "/sys/bus/w1/devices/28-{:012x}/w1_slave",
                config.extra.address
            )),
            current_sensor_index: 0,
            current_data: TemperatureData {
                h2_plate: None,
                batteries: None,
                fuel_cell_controllers: None,
                h2_tanks: None,
                extra: None,
            },
        }
    }

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

    pub fn read(&mut self) -> TemperatureData {
        match self.current_sensor_index {
            0 => self.current_data.h2_plate = self.read_sensor(&self.h2_plate_path),
            1 => self.current_data.batteries = self.read_sensor(&self.batteries_path),
            2 => {
                self.current_data.fuel_cell_controllers =
                    self.read_sensor(&self.fuel_cell_controllers_path)
            }
            3 => self.current_data.h2_tanks = self.read_sensor(&self.h2_tanks_path),
            4 => self.current_data.extra = self.read_sensor(&self.extra_path),
            _ => panic!("Temperature sensor index should not be > 4."),
        };

        self.current_sensor_index += 1;
        if self.current_sensor_index > 4 {
            self.current_sensor_index = 0;
        }

        self.current_data
    }
}
