use super::sensor_data::SensorData;
use crate::devices::Exception;

pub const MIN_THREAD_DELAY_S: f32 = 0.5;

pub trait Sensor {
    type Config;

    /// Creates an appropriate handle to the device. Called once when the program is loaded. Should
    /// panic if there is an IO error (i.e. permission denied) preventing us from reading the
    /// device.
    fn new(config: &Self::Config) -> Self;

    /// Should always timeout after 1.5s at most. Performs necessary checks
    fn read(&mut self) -> (SensorData, Option<Exception>);
}
