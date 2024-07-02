use serde::Deserialize;
use std::fs;

use crate::devices::temperature::TemperatureSensorName;

const fn default_true() -> bool {
    true
}

#[derive(Deserialize, Debug)]
pub struct ContactorConfig {
    pub pin: u8,
    pub normally_open: bool,
}

#[derive(Deserialize, Debug)]
pub struct SerialConfig {
    pub port: String,
    pub baudrate: u32,
}

#[derive(Deserialize, Debug)]
pub struct FuelCellConfig {
    pub serial: SerialConfig,

    pub warn_temperature: f32,
    pub alert_temperature: f32,
    pub critical_temperature: f32,
}

#[derive(Deserialize, Debug)]
pub struct ManometerConfig {
    pub channel: u8,
    pub max_bar: f32,

    pub max_delta: f32,

    pub warn_pressure: f32,
    pub alert_pressure: f32,
    pub critical_pressure: f32,
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

    pub warn: f32,
    pub alert: f32,
    pub max: f32,
}

#[derive(Deserialize, Debug, Clone)]
pub struct BatteryGaugeConfig {
    pub i2c_address: u8,
    pub warning_level: f32,
    pub alert_level: f32,
    pub critical_level: f32,
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
    #[serde(default = "default_true")]
    pub normally_open: bool,
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
    pub dms: ButtonConfig,

    pub telemetry: TelemetryConfig,

    pub fca_relay: ContactorConfig,
    pub fcb_relay: ContactorConfig,
    pub source_isolation_contactor: ContactorConfig,
    pub level2_charge_contactor: ContactorConfig,
}

pub fn load_config(file_path: &str) -> Config {
    let file_contents = fs::read_to_string(file_path).expect("Failed to open config file.");
    toml::from_str(&file_contents).expect("Failed to parse config.")
}
