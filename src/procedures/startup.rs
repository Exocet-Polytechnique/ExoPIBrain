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

struct FuelCellStarter {
    fuel_cell: Arc<RwLock<FuelCell>>,
    relay: Arc<Mutex<Contactor>>,

    reset: bool,
}

impl FuelCellStarter {
    pub fn start(
        fuel_cell: Arc<RwLock<FuelCell>>,
        relay: Arc<Mutex<Contactor>>,
    ) -> Option<FuelCellStarter> {
        relay.lock().unwrap().close_circuit();
        sleep(Duration::from_secs_f32(5.0));

        if fuel_cell.write().unwrap().start().is_err() {
            relay.lock().unwrap().open_circuit();
            return None;
        }

        Some(FuelCellStarter {
            fuel_cell,
            relay,
            reset: true,
        })
    }

    pub fn ok(&mut self) {
        self.reset = false;
    }
}

impl Drop for FuelCellStarter {
    fn drop(&mut self) {
        if self.reset {
            let _ = self.fuel_cell.write().unwrap().shutdown();
            self.relay.lock().unwrap().open_circuit();
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
    let mut mv01_actuator_binding = mv01_actuator.lock().unwrap();
    let mut mv02_actuator_binding = mv02_actuator.lock().unwrap();

    let valve_starter = ValveStarter::start(&mut mv01_actuator_binding, &mut mv02_actuator_binding);
    if !valve_starter.is_some() {
        return false;
    }

    // 5. Open the source isolation contactor for safety
    source_contactor.lock().unwrap().open_circuit();
    sleep(Duration::from_secs_f32(1.0));

    // 6. Startup fuel cells
    let fca_starter = FuelCellStarter::start(fuel_cell_a, fca_relay);
    if !fca_starter.is_some() {
        return false;
    }

    let fcb_starter = FuelCellStarter::start(fuel_cell_b, fcb_relay);
    if !fcb_starter.is_some() {
        return false;
    }

    // 7. DC-DC precharge
    charge_contactor.lock().unwrap().open_circuit();
    sleep(Duration::from_secs_f32(1.0));
    source_contactor.lock().unwrap().close_circuit();
    sleep(Duration::from_secs_f32(40.0));
    charge_contactor.lock().unwrap().close_circuit();
    sleep(Duration::from_secs_f32(1.0));

    // 8. everything ok, keep as-is (i.e. don't reset upon exiting the function)
    valve_starter.unwrap().ok();
    fca_starter.unwrap().ok();
    fcb_starter.unwrap().ok();

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
        let current_data = self.current_data.clone();
        let fuel_cell_a = self.fuel_cell_a.clone();
        let fuel_cell_b = self.fuel_cell_b.clone();
        let fca_relay = self.fca_relay.clone();
        let fcb_relay = self.fcb_relay.clone();
        let mv01_actuator = self.mv01_actuator.clone();
        let mv02_actuator = self.mv02_actuator.clone();
        let source_contactor = self.source_contactor.clone();
        let charge_contactor = self.charge_contactor.clone();
        let dms = self.dms.clone();

        let error_sender = self.error_sender.clone();

        self.handle = Some(thread::spawn(move || {
            // 1. check dms
            if start(
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
            ) {
                let _ =
                    error_sender.send(Message::new(Name::System, Exception::InfoStartupSuccess));
            } else {
                let _ = error_sender.send(Message::new(Name::System, Exception::InfoStartupFailed));
            }
        }));
    }
}
