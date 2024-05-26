use std::time::Instant;

use rppal::gpio::{Gpio, InputPin, Level};
use serde::Deserialize;

#[derive(Deserialize)]
pub struct PrechargeConfig {
    charge_contactor_pin: u8,
    source_isolation_contactor_pin: u8,
    dead_mans_switch_pin: u8,
    precharge_duration_s: f32,
}

fn wait_dms(dms_pin: &InputPin, delay: f32) -> bool {
    let start = Instant::now();

    // for extra security, we'll check first (i.e. if delay is very small)
    if dms_pin.read() == Level::Low {
        return false;
    }

    while start.elapsed().as_secs_f32() < delay {
        if dms_pin.read() == Level::Low {
            return false;
        }
    }

    true
}

/// Returns false if the dms is disconnected at any point
pub fn precharge(pins: &mut Gpio, config: PrechargeConfig) -> bool {
    let dms_pin = pins.get(config.dead_mans_switch_pin).unwrap().into_input();

    let mut source_isolation_contactor_pin = pins
        .get(config.source_isolation_contactor_pin)
        .unwrap()
        .into_output();

    source_isolation_contactor_pin.set_high();
    source_isolation_contactor_pin.set_reset_on_drop(false);

    let precharge_success = wait_dms(&dms_pin, config.precharge_duration_s);

    if precharge_success {
        let mut charge_contactor_pin = pins.get(config.charge_contactor_pin).unwrap().into_output();
        charge_contactor_pin.set_high();
        charge_contactor_pin.set_reset_on_drop(false);
    }

    precharge_success
}
