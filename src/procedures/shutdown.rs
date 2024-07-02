use std::{
    sync::{mpsc::Sender, Arc, Mutex, RwLock},
    thread::JoinHandle,
};

use crate::devices::{
    actuator::Actuator, common::message::Message, contactor::Contactor, fuel_cell::FuelCell,
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
        // TODO:
        // See `startup.rs`, `pub fn start()...` in `impl BoatStarter`
        // we need to:
        // 1. cutoff the charge contactor, then source contactor
        // 2. perform shutdown procedure for fuel cells, including cutting their power with the
        //    fca/b relays (see FC documentation on teams)
        // 3. do an inverse procedure for valves (talk to Emile)
        // send a `InfoShutdownFailed` exception in `error_sendor` in case of any problems and
        // `InfoShutdownSuccess` in case of success, (message name = `System`, see
        // `BoatStarter::start()`)
    }
}
