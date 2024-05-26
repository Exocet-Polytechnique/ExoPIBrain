use std::path::Path;
use std::sync::mpsc::Sender;

use rppal::uart::{Parity, Uart};

use super::common::exceptions::DeviceException;
use crate::config::FuelCellConfig;

pub struct FuelCell {
    started: bool,
    uart_device: Uart,
    data: Option<FuelCellData>,
}

pub struct FuelCellData {
    temperature: f32,
}

impl FuelCell {
    pub fn initialize(config: &FuelCellConfig, error_tx: Sender<DeviceException>) -> FuelCell {
        let uart_device = Uart::with_path(
            Path::new(&config.serial.port),
            config.serial.baudrate,
            Parity::None,
            8,
            1,
        )
        .unwrap();

        FuelCell {
            started: false,
            uart_device,
            data: None,
        }
    }

    pub fn run(&mut self) -> () {
        loop {
            // 0. verifier qu'on ne fait pas de shutdown
            // 1. lire donnees (timeout 1.2s)
            // 2. faire les checks + efficiency
            // 3. attendre read_interval
        }
    }

    pub fn get_temperature(&self) -> Option<f32> {
        Some(self.data.as_ref()?.temperature)
    }
}
