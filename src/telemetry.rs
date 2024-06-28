use std::{env, fs::File, io::Read};

use crate::{
    config::TelemetryConfig,
    devices::{
        battery::BatteryGaugeData,
        common::serial_device::SerialDevice,
        fuel_cell::FuelCellData,
        gps::GpsData,
        temperature::{TemperatureData, TemperatureSensorName},
        Exception,
    },
};
use serde::Serialize;

pub struct Telemetry {
    serial_device: SerialDevice,
    data: FinalTelemetryData,
}

pub struct TelemetryData {
    pub battery: Option<BatteryGaugeData>,
    pub fuel_cell_a: Option<FuelCellData>,
    pub fuel_cell_b: Option<FuelCellData>,
    pub gps: Option<GpsData>,
    pub temperature: TemperatureData,
}

#[derive(Serialize)]
struct FinalTelemetryData {
    pub batt12v_temperature: Option<f32>,
    pub batt12v_voltage: Option<f32>,
    pub batt12v_current: Option<f32>,

    pub batt24v_temperature: Option<f32>,
    pub batt24v_voltage: Option<f32>,
    pub batt24v_current: Option<f32>,

    pub fuellcell_a_temperature: Option<f32>,
    pub fuellcell_b_temperature: Option<f32>,
    pub voltage: Option<f32>,
    pub current: Option<f32>,

    pub lat: Option<f32>,
    pub lon: Option<f32>,

    pub motor_power: Option<f32>,

    pub team: String,
}

fn add_opt(first: Option<f32>, second: Option<f32>) -> Option<f32> {
    Some(first? + second?)
}

fn max_opt(first: Option<f32>, second: Option<f32>) -> Option<f32> {
    if first? > second? {
        first
    } else {
        second
    }
}

impl TelemetryData {
    pub fn new() -> TelemetryData {
        TelemetryData {
            battery: None,
            fuel_cell_a: None,
            fuel_cell_b: None,
            gps: None,
            temperature: TemperatureData::new(),
        }
    }
}

impl FinalTelemetryData {
    fn none() -> Self {
        Self {
            batt12v_temperature: None,
            batt12v_voltage: None,
            batt12v_current: None,

            batt24v_temperature: None,
            batt24v_voltage: None,
            batt24v_current: None,

            fuellcell_a_temperature: None,
            fuellcell_b_temperature: None,
            voltage: None,
            current: None,

            lat: None,
            lon: None,

            motor_power: None,

            team: String::new(),
        }
    }

    fn update(&mut self, data: &TelemetryData) {
        self.batt24v_temperature = *data
            .temperature
            .get(&TemperatureSensorName::Batteries)
            .unwrap_or(&None);
        self.batt24v_voltage = data.battery.map(|x| x.voltage);
        self.batt24v_current = data.battery.map(|x| x.current);

        self.fuellcell_a_temperature = data.fuel_cell_a.and_then(|x| x.temperature);
        self.fuellcell_b_temperature = data.fuel_cell_a.and_then(|x| x.temperature);

        self.voltage = max_opt(
            data.fuel_cell_a.and_then(|a| a.voltage),
            data.fuel_cell_b.and_then(|b| b.voltage),
        );
        self.current = add_opt(
            data.fuel_cell_a.and_then(|a| a.current),
            data.fuel_cell_b.and_then(|b| b.current),
        );

        self.lat = data.gps.map(|x| x.latitude_deg).unwrap_or(None);
        self.lon = data.gps.map(|x| x.longitude_deg).unwrap_or(None);

        self.motor_power = add_opt(
            data.fuel_cell_a.and_then(|a| a.power),
            data.fuel_cell_b.and_then(|b| b.power),
        );
    }
}

impl Telemetry {
    pub fn new(config: &TelemetryConfig) -> Telemetry {
        let serial_device = SerialDevice::initialize(&config.serial);

        let token_file_path = config
            .token_path
            .replace("$HOME", &env::var("HOME").unwrap());

        let mut token_file = File::open(token_file_path).unwrap();
        let mut token_string = String::new();
        token_file.read_to_string(&mut token_string).unwrap();
        let team_token = token_string.trim().to_string();

        let mut data = FinalTelemetryData::none();
        data.team = team_token;

        // Telemetry { serial, data }
        Telemetry {
            serial_device,
            data,
        }
    }

    pub fn send(&mut self, data: &TelemetryData) -> Result<(), Exception> {
        self.data.update(data);

        let json_data = serde_json::to_string(&self.data).map_err(|_| Exception::InfoBadData)?;
        self.serial_device
            .write_null_terminated(json_data.as_bytes())?;

        Ok(())
    }
}
