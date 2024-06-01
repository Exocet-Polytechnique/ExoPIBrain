use std::{
    sync::{mpsc::Sender, Arc, RwLock},
    thread::{self, JoinHandle},
};

use super::{
    exceptions::{DeviceException, SensorMessage},
    sensor::Sensor,
    sensor_data::SensorData,
};

#[derive(Clone)]
pub struct ThreadMessaging {
    pub data_sender: Sender<SensorData>,
    pub error_sender: Sender<SensorMessage>,
    pub stop_signal: Arc<RwLock<bool>>,
}

pub struct SensorThread<T> {
    handle: Option<JoinHandle<()>>,
    messaging: Arc<ThreadMessaging>,
    sensor: Arc<RwLock<T>>,
}

impl<T> SensorThread<T>
where
    T: Sensor + Sync + Send + 'static,
{
    pub fn new(messaging: ThreadMessaging, config: &T::Config) -> Self {
        Self {
            handle: None,
            messaging: Arc::new(messaging),
            sensor: Arc::new(RwLock::new(T::new(config))),
        }
    }

    pub fn start(&mut self) {
        let messaging = self.messaging.clone();
        let sensor_lock = self.sensor.clone();

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
                        .send(SensorMessage {
                            name: T::get_name(),
                            exception: DeviceException::Connected,
                        })
                        .unwrap();
                }
                continue;
            }

            let read_result = sensor.read();

            messaging.data_sender.send(read_result.0);
            if let Some(exception) = read_result.1 {
                messaging
                    .error_sender
                    .send(SensorMessage {
                        name: T::get_name(),
                        exception,
                    })
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
