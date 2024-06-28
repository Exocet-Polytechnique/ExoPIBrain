use std::{
    sync::{Arc, RwLock},
    thread::sleep,
    time::Duration,
};

use crate::{
    devices::{
        actuator::Actuator,
        common::{message::Message, sensor::Sensor, sensor_data::SensorData},
        manometer::Manometer,
        temperature::Temperature,
        Exception, Name,
    },
    interface::{Interface, InterfaceData},
};

fn check_pressure(manometer: Arc<RwLock<Manometer>>) -> Option<f32> {
    let (data, _) = (*manometer).write().unwrap().read();
    match data {
        SensorData::HighPressureManometer(pressure)
        | SensorData::LowPressureManometer(pressure) => pressure,
        _ => panic!("Incorrect return type from high pressure manometer"),
    }
}

fn check_value_under(
    interface: &mut Interface,
    device_name: Name,
    value: Option<f32>,
    max: f32,
) -> bool {
    if let Some(x) = value {
        if x < max {
            return true;
        } else {
            interface.dispatch_message(&Message::new(device_name, Exception::CriticalValue));
        }
    } else {
        interface.dispatch_message(&Message::new(device_name, Exception::InfoBadData));
    }

    false
}

struct ValveStarter<'a> {
    reset: bool,
    mv01_actuator: &'a mut Actuator,
    mv02_actuator: &'a mut Actuator,
}

impl<'a> ValveStarter<'a> {
    fn start(mv01_actuator: &'a mut Actuator, mv02_actuator: &'a mut Actuator) -> Option<Self> {
        if !(!mv01_actuator.is_open() && mv02_actuator.is_open()) {
            return None;
        }

        mv02_actuator.close_valve();
        sleep(Duration::from_millis(2000));

        if !mv02_actuator.is_in_correct_position()
            || !(!mv01_actuator.is_open() && !mv02_actuator.is_open())
        {
            return None;
        }

        mv01_actuator.open_valve();
        sleep(Duration::from_millis(2000));

        if !mv01_actuator.is_in_correct_position()
            || !(mv01_actuator.is_open() && !mv02_actuator.is_open())
        {
            return None;
        }

        Some(ValveStarter {
            reset: true,
            mv01_actuator,
            mv02_actuator,
        })
    }

    fn ok(&mut self) {
        self.reset = false;
    }
}

impl<'a> Drop for ValveStarter<'_> {
    fn drop(&mut self) {
        if self.reset {
            self.mv01_actuator.close_valve();
            sleep(Duration::from_millis(2000));
            self.mv02_actuator.open_valve();
        }
    }
}

pub fn startup(
    interface: &mut Interface,
    high_pressure_manometer: Arc<RwLock<Manometer>>,
    low_pressure_manometer: Arc<RwLock<Manometer>>,
    temperatures: Arc<RwLock<Temperature>>,
    mv01_actuator: &mut Actuator,
    mv02_actuator: &mut Actuator,
) -> bool {
    let mut interface_data = InterfaceData::new();
    let mut can_continue = false;

    // 1. high pressure manometer
    let value = check_pressure(high_pressure_manometer);
    interface_data.high_pressure = value;
    can_continue = check_value_under(interface, Name::HighPressureManometer, value, 300.0);
    interface.render(&interface_data);

    if !can_continue {
        return false;
    }

    // 2. temperature h2 plate
    let value = (*temperatures)
        .write()
        .unwrap()
        .read_sensor(crate::devices::temperature::TemperatureSensorName::H2Plate)
        .ok();
    interface_data.h2_plate_temperature = value;
    can_continue = check_value_under(interface, Name::Temperatures, value, 64.0);
    interface.render(&interface_data);

    if !can_continue {
        return false;
    }

    // 3. valves
    let valve_starter = ValveStarter::start(mv01_actuator, mv02_actuator);
    can_continue = valve_starter.is_some();

    if !can_continue {
        interface.dispatch_message(&Message::new(Name::Pt01Actuator, Exception::AlertStuck));
        interface.render(&interface_data);
        return false;
    }

    // 4. low pressure manometer
    let value = check_pressure(low_pressure_manometer);
    interface_data.low_pressure = value;
    can_continue = check_value_under(interface, Name::LowPressureManometer, value, 0.7);
    interface.render(&interface_data);

    if !can_continue {
        return false;
    }

    valve_starter.unwrap().ok();
    can_continue
}
