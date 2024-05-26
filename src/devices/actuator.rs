use rppal::gpio::{Gpio, InputPin, Level, OutputPin};
use serde::Deserialize;

#[derive(Deserialize)]
pub struct ActuatorConfig {
    control_pin: u8,
    error_pin: u8,
    closed_on_low: bool,
}

pub struct Actuator {
    control_pin: OutputPin,
    error_pin: InputPin,
    closed_on_low: bool,
}

impl Actuator {
    pub fn initialize(pins: &Gpio, config: &ActuatorConfig) -> Actuator {
        // on peut unwrap() ici, car on devrait toujours pouvoir prendre pocession des gpio
        let control_pin = pins.get(config.control_pin).unwrap().into_output();
        let error_pin = pins.get(config.error_pin).unwrap().into_input();

        Actuator {
            control_pin,
            error_pin,
            closed_on_low: config.closed_on_low,
        }
    }

    pub fn open_valve(&mut self) {
        self.control_pin.write(Level::from(self.closed_on_low));
    }

    pub fn close_valve(&mut self) {
        self.control_pin.write(Level::from(!self.closed_on_low));
    }

    pub fn get_status(&self) -> bool {
        self.error_pin.read() == Level::High
    }
}
