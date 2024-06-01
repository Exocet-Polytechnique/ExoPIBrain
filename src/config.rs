use std::fs;

use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct SerialConfig {
    pub port: String,
    pub baudrate: u32,
}

#[derive(Deserialize, Debug)]
pub struct FuelCellConfig {
    priority: u8,
    read_interval: f32,

    pub serial: SerialConfig,
}

#[derive(Deserialize, Debug)]
pub struct ManometerConfig {
    channel: u8,
    max_bar: u16,
}

#[derive(Deserialize, Debug)]
pub struct ManometersConfig {
    priority: u8,
    read_interval: f32,

    high_pressure: ManometerConfig,
    low_pressure: ManometerConfig,
}

#[derive(Deserialize, Debug)]
pub struct TemperatureSensorConfig {
    warn: u8,
    alert: u8,
    max: u8,
    pub address: u64,
}

#[derive(Deserialize, Debug)]
pub struct TemperatureSensorsConfig {
    priority: u8,
    read_interval: f32,

    pub h2_plate: TemperatureSensorConfig,
    pub batteries: TemperatureSensorConfig,
    pub fuel_cell_controllers: TemperatureSensorConfig,
    pub h2_tanks: TemperatureSensorConfig,
    pub extra: TemperatureSensorConfig,
}

#[derive(Deserialize, Debug)]
pub struct BatteryGaugeConfig {
    priority: u8,
    read_interval: f32,
    i2c_address: u8,
    select_gpio: u8,
    warn: u16,
    alert: u16,
    max: u16,
}

#[derive(Deserialize, Debug)]
pub struct GpsConfig {
    pub priority: u8,
    pub read_interval: f32,
    pub serial: SerialConfig,
}

#[derive(Deserialize, Debug)]
pub struct ActuatorConfig {
    pub control_pin: u8,
    pub error_pin: u8,
    pub closed_on_low: bool,
}

#[derive(Deserialize, Debug)]
pub struct TelemetryConfig {
    pub serial: SerialConfig,
    pub send_interval: f32,
    pub token_path: String,
}

#[derive(Deserialize, Debug)]
pub struct Config {
    fuel_cell_a: FuelCellConfig,
    fuel_cell_b: FuelCellConfig,
    manometers: ManometersConfig,
    pub temperatures: TemperatureSensorsConfig,
    battery_gauge: BatteryGaugeConfig,
    pub valve1: ActuatorConfig,
    pub telemetry: TelemetryConfig,
    pub gps: GpsConfig,
}

pub fn load_config(file_path: &str) -> Config {
    let file_contents = fs::read_to_string(file_path).expect("Failed to open config file.");

    match toml::from_str(&file_contents) {
        Err(e) => panic!("Invalid config format:\n{}", e.message()),
        Ok(x) => x,
    }
}
