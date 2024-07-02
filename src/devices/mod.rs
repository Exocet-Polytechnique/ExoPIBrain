use std::io;

pub mod actuator;
pub mod battery;
pub mod button;
pub mod common;
pub mod contactor;
pub mod fuel_cell;
pub mod gps;
pub mod imu;
pub mod manometer;
pub mod temperature;

/// Possible devices from which messages could come
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
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

    /// Dms
    Dms,

    /// Actuators
    Pt01Actuator,
    Pt02Actuator,

    /// Procedures
    System,
}

/// Possible exceptions which can occur while operating the boat
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Exception {
    /// Pilot should evacuate immediatly
    CriticalErrorExit = 0x10,

    /// Boat shutdown
    CriticalValue = 0x11,
    CriticalTemperature = 0x12,
    CriticalPressure = 0x13,
    CriticalCharge = 0x14,
    StartupError = 0x20,
    ShutdownError = 0x21,
    CriticalError = 0x30,

    /// Alert messages
    AlertTemperature = 0x31,
    AlertPressure = 0x32,
    AlertCharge = 0x33,
    AlertStuck = 0x3A,
    AlertNoDms = 0x40,
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
    InfoStartupFailed = 0xB0,
    InfoStartupSuccess = 0xB1,
    InfoShutdownFailed = 0xB2,
    InfoShutdownSuccess = 0xB3,
    Info = 0xC0,
}

impl From<rppal::i2c::Error> for Exception {
    fn from(_value: rppal::i2c::Error) -> Self {
        Self::InfoNotConnected
    }
}

impl From<rppal::uart::Error> for Exception {
    fn from(_value: rppal::uart::Error) -> Self {
        Self::InfoNotConnected
    }
}

impl From<rppal::spi::Error> for Exception {
    fn from(_value: rppal::spi::Error) -> Self {
        Self::InfoNotConnected
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
