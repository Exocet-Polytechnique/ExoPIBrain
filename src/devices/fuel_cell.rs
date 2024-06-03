use std::path::Path;
use std::sync::mpsc::Sender;

use rppal::uart::{Parity, Uart};

use crate::config::FuelCellConfig;

use super::Exception;

pub struct FuelCell {
    started: bool,
    uart_device: Uart,
    data: Option<FuelCellData>,
}

#[derive(Debug, Clone, Copy)]
pub struct FuelCellData {
    pub temperature: f32,
    pub voltage: f32,
    pub current: f32,
    pub power: f32,
}

impl FuelCell {
    pub fn initialize(config: &FuelCellConfig, error_tx: Sender<Exception>) -> FuelCell {
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

    fn write(&mut self, command: String) -> rppal::uart::Result<()> {
        self.uart_device.write((command + "\r").as_bytes())?;
        Ok(())
    }

    pub fn start(&mut self) {
        self.write("start".to_string());
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
