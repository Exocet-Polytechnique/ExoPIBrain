use std::{thread::sleep, time::Duration};

use crate::config::FuelCellConfig;

use super::{
    common::{sensor::Sensor, sensor_data::SensorData, serial_device::SerialDevice},
    Exception,
};

pub enum FuelCellName {
    A,
    B,
}

pub struct FuelCell {
    serial_device: SerialDevice,
    name: FuelCellName,
    is_started: bool,

    warning_temperature: f32,
    alert_temperature: f32,
    critical_temperature: f32,
}

#[derive(Debug, Clone, Copy, Default)]
pub struct FuelCellData {
    pub temperature: Option<f32>,
    pub voltage: Option<f32>,
    pub current: Option<f32>,
    pub power: Option<f32>,
    pub energy: Option<f32>,
}

fn get_value_without_unit(value_str: &str) -> Option<f32> {
    Some(value_str.trim().split_once(' ')?.0.parse().ok()?)
}

fn max_opt(first: Option<f32>, second: Option<f32>) -> Option<f32> {
    if let Some(value1) = first {
        if let Some(value2) = second {
            Some((value1 + value2) / 2.0)
        } else {
            first
        }
    } else {
        second
    }
}

impl FuelCell {
    fn read_raw_data(&mut self) -> Result<FuelCellData, Exception> {
        if !self.is_started {
            return Err(Exception::InfoNotConnected);
        }

        let data_string = self.serial_device.read_until('!', 1.0)?;

        let mut data = FuelCellData::default();

        let mut temperature1 = None;
        let mut temperature2 = None;

        for value_str in data_string.split('|') {
            if let Some((name, value)) = value_str.split_once(':') {
                match name.trim() {
                    "FC_V" => data.voltage = get_value_without_unit(value),
                    "FC_A" => data.current = get_value_without_unit(value),
                    "FCT1" => temperature1 = get_value_without_unit(value),
                    "FCT2" => temperature2 = get_value_without_unit(value),
                    "FC_W" => data.power = get_value_without_unit(value),
                    "Energy" => data.energy = get_value_without_unit(value),
                }
            }
        }

        data.temperature = max_opt(temperature1, temperature2);

        Ok(data)
    }

    fn start(&mut self) -> Result<(), Exception> {
        self.serial_device.writeln("start".to_string());

        let mut temperature_ok = false;
        let mut pressure_ok = false;

        let mut attempts = 5;

        while !temperature_ok || !pressure_ok {
            let data = self.serial_device.readln(10.0)?;
            if data.contains("Anode Supply Pressure OK") {
                pressure_ok = true;
            } else if data.contains("Temperature Check OK") {
                temperature_ok = true;
            }

            sleep(Duration::from_millis(200));

            attempts -= 1;
            if attempts <= 0 {
                return Err(Exception::StartupError);
            }
        }

        self.is_started = true;

        Ok(())
    }

    fn shutdown(&mut self) -> Result<(), Exception> {
        self.serial_device.writeln("end".to_string());

        let mut system_off = false;

        let mut attempts = 5;

        while !system_off {
            let data = self.serial_device.readln(10.0)?;
            if data.contains("System Off") {
                system_off = true;
            }

            sleep(Duration::from_millis(200));

            attempts -= 1;
            if attempts <= 0 {
                return Err(Exception::ShutdownError);
            }
        }

        self.is_started = true;

        Ok(())
    }

    fn purge(&mut self) -> Result<(), Exception> {
        self.serial_device.writeln("p".to_string())?;

        Ok(())
    }

    fn check_temperature(&self, temperature: f32) -> Option<Exception> {
        if temperature > self.critical_temperature {
            Some(Exception::CriticalTemperature)
        } else if temperature > self.alert_temperature {
            Some(Exception::AlertTemperature)
        } else if temperature > self.warning_temperature {
            Some(Exception::WarningTemperature)
        } else {
            None
        }
    }
}

impl Sensor for FuelCell {
    type Config = (FuelCellConfig, FuelCellName);

    fn new(config: &Self::Config) -> Self {
        let serial_device = SerialDevice::initialize(&config.0.serial);

        FuelCell {
            serial_device,
            name: config.1,
            is_started: false,

            warning_temperature: config.0.warn_temperature,
            alert_temperature: config.0.alert_temperature,
            critical_temperature: config.0.critical_temperature,
        }
    }

    fn read(&mut self) -> (SensorData, Option<Exception>) {
        let fuel_cell_data = self.read_raw_data();

        let sensor_data = match self.name {
            A => SensorData::FuelCellA(fuel_cell_data.ok()),
            B => SensorData::FuelCellB(fuel_cell_data.ok()),
        };

        if let Ok(data) = fuel_cell_data {
            if let Some(temperature) = data.temperature {
                return (sensor_data, self.check_temperature(temperature));
            } else {
                return (sensor_data, Some(Exception::InfoBadData));
            }
        }

        (sensor_data, fuel_cell_data.err())
    }
}
