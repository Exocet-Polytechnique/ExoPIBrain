use std::{
    sync::{mpsc::Sender, Arc, RwLock},
    thread::{self, JoinHandle},
};

use crate::devices::{Exception, Name};

use super::{message::Message, sensor::Sensor, sensor_data::SensorData};

#[derive(Clone)]
pub struct ThreadMessaging {
    pub data_sender: Sender<SensorData>,
    pub error_sender: Sender<Message>,
    pub stop_signal: Arc<RwLock<bool>>,
}

pub struct SensorThread<T> {
    handle: Option<JoinHandle<()>>,
    messaging: Arc<ThreadMessaging>,
    sensor: Arc<RwLock<T>>,
    device_name: Name,
}

impl<T> SensorThread<T>
where
    T: Sensor + Sync + Send + 'static,
{
    pub fn new(messaging: ThreadMessaging, config: &T::Config, name: Name) -> Self {
        Self {
            handle: None,
            messaging: Arc::new(messaging),
            sensor: Arc::new(RwLock::new(T::new(config))),
            device_name: name,
        }
    }

    pub fn start(&mut self) {
        let messaging = self.messaging.clone();
        let sensor_lock = self.sensor.clone();
        let device_name = self.device_name.clone();

        self.handle = Some(thread::spawn(move || loop {
            {
                if *messaging.stop_signal.read().unwrap() {
                    break;
                }
            }

            let mut sensor = (*sensor_lock).write().unwrap();

            if !sensor.is_connected() {
                sensor.intialize();

                if sensor.is_connected() {
                    messaging
                        .error_sender
                        .send(Message::new(device_name, Exception::InfoConnected))
                        .unwrap();
                }
                continue;
            }

            let read_result = sensor.read();

            messaging.data_sender.send(read_result.0).unwrap();
            if let Some(exception) = read_result.1 {
                messaging
                    .error_sender
                    .send(Message::new(device_name, exception))
                    .unwrap();
            }
        }))
    }

    pub fn is_stopped(&self) -> bool {
        if let Some(handle) = &self.handle {
            handle.is_finished()
        } else {
            true
        }
    }
}
