use super::sensor_data::SensorData;
use crate::devices::Exception;

pub trait Sensor {
    type Config;

    /// Creates an appropriate handle to the device. Called once when the program is loaded. Should
    /// panic if there is an IO error (i.e. permission denied) preventing us from reading the
    /// device.
    fn new(config: &Self::Config) -> Self;

    fn is_connected(&self) -> bool {
        true
    }

    fn intialize(&mut self) {}
    fn shutdown(&mut self) {}

    /// Should always timeout after 1.5s at most. Performs necessary checks
    fn read(&mut self) -> (SensorData, Option<Exception>);
}
