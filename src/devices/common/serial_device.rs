use std::{path::Path, sync::Mutex, time::Duration};

use rppal::uart::{Parity, Uart};

use crate::config::SerialConfig;

use super::exceptions::DeviceException;

const BASE_LINE_LENGTH: usize = 256; // optimize line strings

pub enum SerialError {
    IoError,
}

pub struct SerialDevice {
    device: Mutex<Uart>,
}

impl SerialDevice {
    pub fn initialize(config: &SerialConfig) -> SerialDevice {
        let device = Mutex::new(
            Uart::with_path(Path::new(&config.port), config.baudrate, Parity::None, 8, 1).unwrap(),
        );

        SerialDevice { device }
    }

    pub fn writeln(&mut self, command: String) -> Result<(), SerialError> {
        self.device
            .lock()
            .unwrap()
            .write((command + "\r").as_bytes())?;
        Ok(())
    }

    pub fn readln(&self, timeout: f32) -> Result<String, DeviceException> {
        let mut line = String::with_capacity(BASE_LINE_LENGTH);

        let mut device = self.device.lock().unwrap();

        // TODO: make sure the timeout works
        device.set_read_mode(0, Duration::from_secs_f32(timeout))?;

        let mut buffer = [0u8; 1];
        while buffer[0] != b'\n' && buffer[0] != b'\r' {
            device.read(&mut buffer)?;
            line.push(buffer[0] as char);
        }

        Ok(line)
    }
}

impl From<rppal::uart::Error> for SerialError {
    fn from(value: rppal::uart::Error) -> Self {
        match value {
            // TODO:
            _ => panic!("Unexpected error when writing to serial device."),
        }
    }
}
