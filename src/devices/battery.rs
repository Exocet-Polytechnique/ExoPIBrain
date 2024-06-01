use rppal::i2c::I2c;
use std::{
    ops::DerefMut,
    sync::{Arc, Mutex},
    thread,
};

use crate::config::BatteryGaugeConfig;

use super::common::exceptions::DeviceException;

const DEVICE_ADDRESS: u16 = 0x64;
const CONTROL_REGISTER: u8 = 0x01;
// ADC mode: sleep: prescaler: 1024, ALCC disabled
const INITIAL_CONFIGURATION: u8 = 0b00101000;
const REQUEST_ADC_UPDATE: u8 = 0b01101000;

const ADC_UPDATE_DELAY_MS: u64 = 50;

pub struct BatteryGauge {
    bus: Arc<Mutex<I2c>>,
}

#[derive(Debug)]
pub struct BatteryGaugeData {
    voltage: f32,
    current: f32,
    charge_level: f32,
}

impl BatteryGauge {
    pub fn initialize(config: &BatteryGaugeConfig, bus: Arc<Mutex<I2c>>) -> BatteryGauge {
        BatteryGauge { bus }
    }

    pub fn try_connect(&mut self) -> Result<(), DeviceException> {
        let mut bus_lock = self.bus.lock().unwrap();
        (*bus_lock).set_slave_address(DEVICE_ADDRESS)?;
        (*bus_lock).smbus_write_byte(CONTROL_REGISTER, INITIAL_CONFIGURATION)?;

        Ok(())
    }

    pub fn read(&mut self) -> Result<BatteryGaugeData, DeviceException> {
        let mut bus_lock = self.bus.lock().unwrap();
        (*bus_lock).set_slave_address(DEVICE_ADDRESS)?;
        (*bus_lock).smbus_write_byte(CONTROL_REGISTER, REQUEST_ADC_UPDATE)?;
        thread::sleep(std::time::Duration::from_millis(ADC_UPDATE_DELAY_MS));

        // p. 9 and 13 (r_sense = 1 mOhm)
        let voltage_data = (*bus_lock).smbus_read_word_swapped(0x08)? as u16;
        let voltage = (voltage_data as f32) / (u16::MAX as f32) * 70.8;

        let current_data = (*bus_lock).smbus_read_word_swapped(0x0E)? as i16;
        let current = 64.0 * (((current_data - i16::MAX) as f32) / (i16::MAX as f32));

        // NOTE: 1. j'assume que la batterie est chargee a 80% au demarrage
        // NOTE: 2. j'assume aussi que le compteur de coulomb decremente quand on decharge la
        // batterie
        let coulomb_data = (*bus_lock).smbus_read_word_swapped(0x02)?;
        let coulomb_count = (32767 - coulomb_data as u32) * 1024;
        let charge_level = ((43200.0 - coulomb_count as f32) / 86400.0) * 100.0;

        Ok(BatteryGaugeData {
            voltage,
            current,
            charge_level,
        })
    }
}
