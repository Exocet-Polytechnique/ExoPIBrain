use crate::devices::{
    battery::BatteryGaugeData,
    fuel_cell::FuelCellData,
    gps::GpsData,
    imu::{AccelerometerData, CompassData, GyroscopeData},
    temperature::TemperatureSensorName,
};

/// Possible data types that can be returned from the Sensor's `read()` method
#[derive(Debug)]
pub enum SensorData {
    FuelCellA(Option<FuelCellData>),
    FuelCellB(Option<FuelCellData>),

    Temperature((TemperatureSensorName, Option<f32>)),

    HighPressureManometer(Option<f32>),
    LowPressureManometer(Option<f32>),

    Batteries(Option<BatteryGaugeData>),

    Accelerometer(Option<AccelerometerData>),
    Gyroscope(Option<GyroscopeData>),
    Compass(Option<CompassData>),

    Gps(Option<GpsData>),
}
