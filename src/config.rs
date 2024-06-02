use serde::Deserialize;
use std::fs;

use crate::devices::temperature::TemperatureSensorName;

#[derive(Deserialize, Debug)]
pub struct SerialConfig {
    pub port: String,
    pub baudrate: u32,
}

#[derive(Deserialize, Debug)]
pub struct FuelCellConfig {
    pub serial: SerialConfig,
}

#[derive(Deserialize, Debug)]
pub struct ManometerConfig {
    pub channel: u8,
    pub max_bar: f32,

    pub max_delta: f32,
}

#[derive(Deserialize, Debug)]
pub struct ActuatorConfig {
    pub control_pin: u8,
    pub error_pin: u8,
    pub normally_open: bool,
}

#[derive(Deserialize, Debug)]
pub struct TemperatureConfig {
    pub name: TemperatureSensorName,
    pub address: u64,

    pub warn: u8,
    pub alert: u8,
    pub max: u8,
}

#[derive(Deserialize, Debug)]
pub struct BatteryGaugeConfig {
    i2c_address: u8,
}

#[derive(Deserialize, Debug)]
pub struct AccelerometerConfig {
    i2c_address: u8,
}

#[derive(Deserialize, Debug)]
pub struct GyroscopeConfig {
    i2c_address: u8,
}

#[derive(Deserialize, Debug)]
pub struct CompassConfig {
    i2c_address: u8,
}

#[derive(Deserialize, Debug)]
pub struct GpsConfig {
    pub serial: SerialConfig,
}

#[derive(Deserialize, Debug)]
pub struct ButtonConfig {
    pub pin: u8,
}

#[derive(Deserialize, Debug)]
pub struct TelemetryConfig {
    pub serial: SerialConfig,

    pub send_interval: f32,
    pub token_path: String,
}

#[derive(Deserialize, Debug)]
pub struct Config {
    pub fuel_cell_a: FuelCellConfig,
    pub fuel_cell_b: FuelCellConfig,

    pub high_pressure_manometer: ManometerConfig,
    pub low_pressure_manometer: ManometerConfig,

    pub valve1: ActuatorConfig,
    pub valve2: ActuatorConfig,

    pub temperatures: Vec<TemperatureConfig>,

    pub battery_gauge: BatteryGaugeConfig,

    pub accelerometer: AccelerometerConfig,
    pub gyroscope: GyroscopeConfig,
    pub compass: CompassConfig,

    pub gps: GpsConfig,

    pub start_button: ButtonConfig,
    pub stop_button: ButtonConfig,

    pub telemetry: TelemetryConfig,
}

pub fn load_config(file_path: &str) -> Config {
    let file_contents = fs::read_to_string(file_path).expect("Failed to open config file.");
    toml::from_str(&file_contents).expect("Failed to parse config.")
}
