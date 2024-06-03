use std::io;

pub mod actuator;
pub mod battery;
pub mod common;
pub mod fuel_cell;
pub mod gps;
pub mod imu;
pub mod manometer;
pub mod temperature;

/// Possible devices from which messages could come
#[derive(Clone, Copy)]
pub enum Name {
    /// Fuel cells
    FuelCellA,
    FuelCellB,

    /// Temperature sensors
    Temperatures,

    /// Manometers
    HighPressureManometer,
    LowPressureManometer,

    /// Battery gauge
    BatteryGauge,

    /// IMU
    Accelerometer,
    Gyroscope,
    Compass,

    /// Gps
    Gps,
}

/// Possible exceptions which can occur while operating the boat
#[derive(Debug, Clone, Copy)]
pub enum Exception {
    /// Pilot should evacuate immediatly
    CriticalErrorExit = 0x10,

    /// Boat shutdown
    CriticalTemperature = 0x11,
    CriticalPressure = 0x12,
    CriticalCharge = 0x13,
    CriticalError = 0x30,

    /// Alert messages
    AlertTemperature = 0x31,
    AlertPressure = 0x32,
    AlertCharge = 0x33,
    Alert = 0x50,

    /// Warning messages
    WarningTemperature = 0x51,
    WarningPressure = 0x52,
    WarningCharge = 0x53,
    Warning = 0xA0,

    /// Informational messages
    InfoConnected = 0xA1,
    InfoNotConnected = 0xA2,
    InfoBadData = 0xA3,
    Info = 0xC0,
}

impl From<rppal::i2c::Error> for Exception {
    fn from(value: rppal::i2c::Error) -> Self {
        todo!();
    }
}

impl From<rppal::uart::Error> for Exception {
    fn from(value: rppal::uart::Error) -> Self {
        todo!();
    }
}

impl From<io::Error> for Exception {
    fn from(_: io::Error) -> Self {
        Self::InfoNotConnected
    }
}

impl From<std::num::ParseFloatError> for Exception {
    fn from(_: std::num::ParseFloatError) -> Self {
        Self::InfoBadData
    }
}