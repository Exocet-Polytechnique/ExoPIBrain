use std::{path::Path, time::Duration};

use rppal::uart::{Parity, Uart};

use crate::config::SerialConfig;

const BASE_LINE_LENGTH: usize = 256; // optimize line strings

enum SerialError {
    IoError,
}

pub struct SerialDevice {
    device: Uart,
}

impl SerialDevice {
    pub fn initialize(config: &SerialConfig) -> SerialDevice {
        let mut device =
            Uart::with_path(Path::new(&config.port), config.baudrate, Parity::None, 8, 1).unwrap();
        device.set_read_mode(1, Duration::ZERO);

        SerialDevice { device }
    }

    pub fn writeln(&mut self, command: String) -> Result<(), SerialError> {
        self.device.write((command + "\r").as_bytes())?;
        Ok(())
    }

    pub fn readln(&mut self) -> String {
        let mut line = String::with_capacity(BASE_LINE_LENGTH);

        let mut buffer = [0u8; 1];
        while buffer[0] != b'\n' || buffer[0] != b'\r' {
            self.device.read(&mut buffer);
            line.push(buffer[0] as char);
        }

        line
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
