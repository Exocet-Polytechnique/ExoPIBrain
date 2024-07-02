use rppal::gpio::{Gpio, Level, OutputPin};

use crate::config::ContactorConfig;

pub struct Contactor {
    pin: OutputPin,
    normally_open: bool,
}

impl Contactor {
    pub fn initialize(pins: &Gpio, config: &ContactorConfig) -> Self {
        // on peut unwrap() ici, car on devrait toujours pouvoir prendre pocession des gpio
        let pin = pins.get(config.pin).unwrap().into_output();

        Self {
            pin,
            normally_open: config.normally_open,
        }
    }

    pub fn close_circuit(&mut self) {
        self.pin.write(Level::from(self.normally_open));
    }

    pub fn open_circuit(&mut self) {
        self.pin.write(Level::from(!self.normally_open));
    }
}
