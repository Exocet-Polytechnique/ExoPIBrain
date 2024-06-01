use super::{exceptions::DeviceException, sensor_data::SensorData};

#[derive(Debug)]
pub enum SensorName {
    FuelCellA,
    FuelCellB,
    Gps,
    Batteries,
}

pub trait Sensor {
    type Config;

    fn new(config: &Self::Config) -> Self;

    fn is_connected(&self) -> bool {
        true
    }

    fn intialize(&mut self) {}
    fn shutdown(&mut self) {}

    fn get_name() -> SensorName;

    /// should always timeout after 1.5s at most. Performs necessary checks
    fn read(&self) -> (SensorData, Option<DeviceException>);
}
