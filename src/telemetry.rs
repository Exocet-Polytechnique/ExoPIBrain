use std::{env, fs::File, io::Read};

use crate::config::TelemetryConfig;
use rppal::uart::{Parity, Uart};
use serde::Serialize;
use serde_json::to_string;

#[derive(Serialize)]
struct TelemetryData {
    batt12v_temperature: Option<f32>,
    batt12v_voltage: Option<f32>,
    batt12v_current: Option<f32>,
    batt24v_temperature: Option<f32>,
    batt24v_voltage: Option<f32>,
    batt24v_current: Option<f32>,
    fuellcell_a_temperature: Option<f32>,
    fuellcell_b_temperature: Option<f32>,
    voltage: Option<f32>,
    current: Option<f32>,
    lat: Option<f32>,
    lon: Option<f32>,
    motor_power: Option<f32>,
    team: String,
}

pub struct Telemetry {
    serial: Uart,
    team_token: String,
}

impl Telemetry {
    pub fn new(config: &TelemetryConfig) -> Telemetry {
        let serial = Uart::with_path(
            &config.serial.port,
            config.serial.baudrate,
            Parity::None,
            8,
            1,
        )
        .unwrap();

        let token_file_path = config
            .token_path
            .replace("$HOME", &env::var("HOME").unwrap());

        let mut token_file = File::open(token_file_path).unwrap();
        let mut token_string = String::new();
        token_file.read_to_string(&mut token_string).unwrap();
        let team_token = token_string.trim().to_string();

        Telemetry { serial, team_token }
    }

    pub fn send(&mut self) {}
}
