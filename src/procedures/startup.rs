use std::{
    sync::{mpsc::Sender, Arc, Mutex, RwLock},
    thread::{self, sleep, JoinHandle},
    time::Duration,
};

use crate::devices::{
    actuator::Actuator, button::Button, common::message::Message, contactor::Contactor,
    fuel_cell::FuelCell, Exception, Name,
};

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

#[derive(Default)]
pub struct StartupData {
    pub h2_plate_temperature: Option<f32>,
    pub high_pressure: Option<f32>,
    pub low_pressure: Option<f32>,
}

pub struct BoatStarter {
    error_sender: Sender<Message>,
    current_data: Arc<RwLock<StartupData>>,

    fuel_cell_a: Arc<RwLock<FuelCell>>,
    fuel_cell_b: Arc<RwLock<FuelCell>>,
    fca_relay: Arc<Mutex<Contactor>>,
    fcb_relay: Arc<Mutex<Contactor>>,

    mv01_actuator: Arc<Mutex<Actuator>>,
    mv02_actuator: Arc<Mutex<Actuator>>,

    source_contactor: Arc<Mutex<Contactor>>,
    charge_contactor: Arc<Mutex<Contactor>>,
    dms: Arc<Mutex<Button>>,

    handle: Option<JoinHandle<()>>,
}

fn start(
    current_data: Arc<RwLock<StartupData>>,

    fuel_cell_a: Arc<RwLock<FuelCell>>,
    fuel_cell_b: Arc<RwLock<FuelCell>>,
    fca_relay: Arc<Mutex<Contactor>>,
    fcb_relay: Arc<Mutex<Contactor>>,

    mv01_actuator: Arc<Mutex<Actuator>>,
    mv02_actuator: Arc<Mutex<Actuator>>,

    source_contactor: Arc<Mutex<Contactor>>,
    charge_contactor: Arc<Mutex<Contactor>>,
    dms: Arc<Mutex<Button>>,
) -> bool {
    // 1. check dms
    if dms.lock().unwrap().read() {
        return false;
    }

    // 2. check temperature
    if let Some(temperature) = current_data.read().unwrap().h2_plate_temperature {
        if temperature > 64.0 {
            return false;
        }
    } else {
        return false;
    }

    // 3. check high pressure
    if let Some(pressure) = current_data.read().unwrap().high_pressure {
        if pressure > 300.0 {
            return false;
        }
    } else {
        return false;
    }

    // 4. do valve procedures
    let valve_starter = ValveStarter::start(
        &mut mv01_actuator.lock().unwrap(),
        &mut mv02_actuator.lock().unwrap(),
    );
    if !valve_starter.is_some() {
        return false;
    }

    // 5. TODO: open the source isolation contactor (prevent current from flowing through)
    // 6. TODO: proceed to fuel cell startup (crate a struct similar to `ValveStarter` for this).
    //    Instructions can be found in the fuel cell's datasheet ONLY ONE AT A TIME! Use fca/b_relay
    //    to control power input to the fuel cell controllers as described in the datasheet.
    // 7. TODO: open charge contactor, wait 1 s, then vlose source isolation contactor, wait 30 s,
    //    then close charge contactor, wait 1 s

    // 5. everything ok, keep as-is (i.e. don't reset upon exiting the function)
    valve_starter.unwrap().ok();

    true
}

impl BoatStarter {
    pub fn new(
        error_sender: Sender<Message>,
        current_data: Arc<RwLock<StartupData>>,

        fuel_cell_a: Arc<RwLock<FuelCell>>,
        fuel_cell_b: Arc<RwLock<FuelCell>>,
        fca_relay: Arc<Mutex<Contactor>>,
        fcb_relay: Arc<Mutex<Contactor>>,

        mv01_actuator: Arc<Mutex<Actuator>>,
        mv02_actuator: Arc<Mutex<Actuator>>,

        source_contactor: Arc<Mutex<Contactor>>,
        charge_contactor: Arc<Mutex<Contactor>>,
        dms: Arc<Mutex<Button>>,
    ) -> Self {
        Self {
            error_sender,
            current_data,
            fuel_cell_a,
            fuel_cell_b,
            fca_relay,
            fcb_relay,
            mv01_actuator,
            mv02_actuator,
            source_contactor,
            charge_contactor,
            dms,
            handle: None,
        }
    }

    pub fn start(&mut self) {
        self.handle = Some(thread::spawn(|| {
            // 1. check dms
            if start(
                self.current_data.clone(),
                self.fuel_cell_a.clone(),
                self.fuel_cell_b.clone(),
                self.fca_relay.clone(),
                self.fcb_relay.clone(),
                self.mv01_actuator.clone(),
                self.mv02_actuator.clone(),
                self.source_contactor.clone(),
                self.charge_contactor.clone(),
                self.dms.clone(),
            ) {
                self.error_sender
                    .clone()
                    .send(Message::new(Name::System, Exception::InfoStartupSuccess));
            } else {
                self.error_sender
                    .clone()
                    .send(Message::new(Name::System, Exception::InfoStartupFailed));
            }
        }));
    }
}
