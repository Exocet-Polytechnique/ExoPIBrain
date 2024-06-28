use std::{
    sync::{mpsc::Sender, Arc, RwLock},
    thread::{self, JoinHandle},
    time::{Duration, Instant},
};

use crate::devices::{Exception, Name};

use super::{
    message::Message,
    sensor::{Sensor, MIN_THREAD_DELAY_S},
    sensor_data::SensorData,
};

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
            let start_time = Instant::now();

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

            let remaining_time = MIN_THREAD_DELAY_S - start_time.elapsed().as_secs_f32();
            if remaining_time > 0.0 {
                std::thread::sleep(Duration::from_secs_f32(remaining_time));
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

    pub fn get_sensor(&mut self) -> Arc<RwLock<T>> {
        self.sensor.clone()
    }
}
