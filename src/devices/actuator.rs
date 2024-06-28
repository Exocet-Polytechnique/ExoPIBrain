use rppal::gpio::{Gpio, InputPin, Level, OutputPin};

use crate::config::ActuatorConfig;

pub struct Actuator {
    control_pin: OutputPin,
    error_pin: InputPin,
    normally_open: bool,
}

impl Actuator {
    pub fn initialize(pins: &Gpio, config: &ActuatorConfig) -> Actuator {
        // on peut unwrap() ici, car on devrait toujours pouvoir prendre pocession des gpio
        let control_pin = pins.get(config.control_pin).unwrap().into_output();
        let error_pin = pins.get(config.error_pin).unwrap().into_input();

        Actuator {
            control_pin,
            error_pin,
            normally_open: config.normally_open,
        }
    }

    pub fn open_valve(&mut self) {
        self.control_pin.write(Level::from(self.normally_open));
    }

    pub fn close_valve(&mut self) {
        self.control_pin.write(Level::from(!self.normally_open));
    }

    pub fn is_open(&self) -> bool {
        if self.error_pin.read() == Level::High {
            !self.normally_open
        } else {
            self.normally_open
        }
    }

    pub fn is_in_correct_position(&self) -> bool {
        self.error_pin.read() == Level::Low
    }
}
