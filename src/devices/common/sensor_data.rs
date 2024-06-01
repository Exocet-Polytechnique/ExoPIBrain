use crate::devices::{
    battery::BatteryGaugeData, fuel_cell::FuelCellData, gps::GpsData, imu::ImuData,
};

#[derive(Debug)]
pub enum SensorData {
    FuelCellA(Option<FuelCellData>),
    FuelCellB(Option<FuelCellData>),
    H2PlateTemperature(Option<f32>),
    H2TanksTemperature(Option<f32>),
    FuelCellControllersTemperature(Option<f32>),
    BatteriesTemperture(Option<f32>),
    ExtraTemperature(Option<f32>),
    Imu(Option<ImuData>),
    HighPressureManometer(Option<f32>),
    LowPressureManometer(Option<f32>),
    Gps(Option<GpsData>),
    Batteries(Option<BatteryGaugeData>),
}
