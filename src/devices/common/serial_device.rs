use std::{path::Path, sync::Mutex, time::Duration};

use rppal::uart::{Parity, Uart};

use crate::{config::SerialConfig, devices::Exception};

const BASE_LINE_LENGTH: usize = 256; // optimize line strings

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

    pub fn writeln(&mut self, command: String) -> Result<(), Exception> {
        self.device
            .lock()
            .unwrap()
            .write((command + "\r").as_bytes())?;
        Ok(())
    }

    pub fn write_null_terminated(&mut self, data: &[u8]) -> Result<(), Exception> {
        self.device.lock().unwrap().write(data)?;
        self.device.lock().unwrap().write(&[0])?;

        Ok(())
    }

    fn read_until_predicate(
        &self,
        pred: impl Fn(u8) -> bool,
        timeout: f32,
    ) -> Result<String, Exception> {
        let mut line = String::with_capacity(BASE_LINE_LENGTH);

        let mut device = self.device.lock().unwrap();

        device.set_read_mode(0, Duration::from_secs_f32(timeout))?;

        let mut buffer = [0u8; 1];
        while pred(buffer[0]) {
            let length = device.read(&mut buffer)?;
            if length == 0 {
                return Err(Exception::InfoNotConnected);
            }
            line.push(buffer[0] as char);
        }

        Ok(line)
    }

    pub fn readln(&self, timeout: f32) -> Result<String, Exception> {
        self.read_until_predicate(|c| c != b'\n' && c != b'\r', timeout)
    }

    pub fn read_until(&self, delimiter: char, timeout: f32) -> Result<String, Exception> {
        self.read_until_predicate(|c| c != delimiter as u8, timeout)
    }
}
