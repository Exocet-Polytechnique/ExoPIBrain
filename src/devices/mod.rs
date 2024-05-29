pub mod actuator;
pub mod battery;
pub mod common;
pub mod fuel_cell;
pub mod gps;
pub mod manometer;
pub mod temperature;

use fuel_cell::FuelCellData;

#[derive(Clone, Copy)]
pub struct SensorData {
    pub fuel_cell_a: Option<FuelCellData>,
    pub fuel_cell_b: Option<FuelCellData>,
}

impl Default for SensorData {
    fn default() -> Self {
        SensorData {
            fuel_cell_a: None,
            fuel_cell_b: None,
        }
    }
}
