use rppal::gpio::{Gpio, InputPin, Level};

use crate::config::ButtonConfig;

pub struct Button {
    normally_open: bool,
    pin: InputPin,
}

impl Button {
    pub fn new(pins: &Gpio, config: &ButtonConfig) -> Self {
        let pin = pins.get(config.pin).unwrap().into_input();

        Self {
            normally_open: config.normally_open,
            pin,
        }
    }

    pub fn read(&mut self) -> bool {
        if self.pin.read() == Level::High {
            self.normally_open
        } else {
            !self.normally_open
        }
    }
}
