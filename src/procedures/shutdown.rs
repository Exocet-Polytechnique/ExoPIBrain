use std::{
    sync::{mpsc::Sender, Arc, Mutex, RwLock},
    thread::{self, sleep, JoinHandle},
    time::Duration,
};

use crate::devices::{
    actuator::Actuator, common::message::Message, contactor::Contactor, fuel_cell::FuelCell,
    Exception, Name,
};

pub struct BoatStopper {
    error_sender: Sender<Message>,

    fuel_cell_a: Arc<RwLock<FuelCell>>,
    fuel_cell_b: Arc<RwLock<FuelCell>>,
    fca_relay: Arc<Mutex<Contactor>>,
    fcb_relay: Arc<Mutex<Contactor>>,

    mv01_actuator: Arc<Mutex<Actuator>>,
    mv02_actuator: Arc<Mutex<Actuator>>,

    source_contactor: Arc<Mutex<Contactor>>,
    charge_contactor: Arc<Mutex<Contactor>>,

    handle: Option<JoinHandle<()>>,
}

fn shutdown(
    fuel_cell_a: Arc<RwLock<FuelCell>>,
    fuel_cell_b: Arc<RwLock<FuelCell>>,
    fca_relay: Arc<Mutex<Contactor>>,
    fcb_relay: Arc<Mutex<Contactor>>,

    mv01_actuator: Arc<Mutex<Actuator>>,
    mv02_actuator: Arc<Mutex<Actuator>>,

    source_contactor: Arc<Mutex<Contactor>>,
    charge_contactor: Arc<Mutex<Contactor>>,
) -> bool {
    // 1. Disconnect dc-dc from fuel cells
    source_contactor.lock().unwrap().open_circuit();
    sleep(Duration::from_secs_f32(1.0));
    charge_contactor.lock().unwrap().open_circuit();

    // 2. Shutdown fuel cells
    sleep(Duration::from_secs_f32(10.0)); // wait a bit for fuel cell to cool down
    if fuel_cell_a.write().unwrap().shutdown().is_err() {
        return false;
    }
    if fuel_cell_b.write().unwrap().shutdown().is_err() {
        return false;
    }

    // 3. Reset valves
    mv01_actuator.lock().unwrap().close_valve();
    sleep(Duration::from_secs_f32(2.0));
    if !mv01_actuator.lock().unwrap().is_in_correct_position() {
        // NOTE: EXTREMELY DANGEROUS
        return false;
    }

    mv02_actuator.lock().unwrap().open_valve();
    sleep(Duration::from_secs_f32(2.0));
    if !mv02_actuator.lock().unwrap().is_in_correct_position() {
        return false;
    }

    // 4. Disconnect Fuel Cell power supply
    fca_relay.lock().unwrap().open_circuit();
    fcb_relay.lock().unwrap().open_circuit();

    true
}

impl BoatStopper {
    pub fn new(
        error_sender: Sender<Message>,
        fuel_cell_a: Arc<RwLock<FuelCell>>,
        fuel_cell_b: Arc<RwLock<FuelCell>>,
        fca_relay: Arc<Mutex<Contactor>>,
        fcb_relay: Arc<Mutex<Contactor>>,

        mv01_actuator: Arc<Mutex<Actuator>>,
        mv02_actuator: Arc<Mutex<Actuator>>,

        source_contactor: Arc<Mutex<Contactor>>,
        charge_contactor: Arc<Mutex<Contactor>>,
    ) -> Self {
        Self {
            error_sender,
            fuel_cell_a,
            fuel_cell_b,
            fca_relay,
            fcb_relay,
            mv01_actuator,
            mv02_actuator,
            source_contactor,
            charge_contactor,
            handle: None,
        }
    }

    pub fn stop(&mut self) {
        let fuel_cell_a = self.fuel_cell_a.clone();
        let fuel_cell_b = self.fuel_cell_b.clone();
        let fca_relay = self.fca_relay.clone();
        let fcb_relay = self.fcb_relay.clone();
        let mv01_actuator = self.mv01_actuator.clone();
        let mv02_actuator = self.mv02_actuator.clone();
        let source_contactor = self.source_contactor.clone();
        let charge_contactor = self.charge_contactor.clone();

        let error_sender = self.error_sender.clone();

        self.handle = Some(thread::spawn(move || {
            // 1. check dms
            if shutdown(
                fuel_cell_a,
                fuel_cell_b,
                fca_relay,
                fcb_relay,
                mv01_actuator,
                mv02_actuator,
                source_contactor,
                charge_contactor,
            ) {
                let _ =
                    error_sender.send(Message::new(Name::System, Exception::InfoShutdownSuccess));
            } else {
                let _ =
                    error_sender.send(Message::new(Name::System, Exception::InfoShutdownFailed));
            }
        }));
    }
}
