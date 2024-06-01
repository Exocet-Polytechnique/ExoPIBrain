#[derive(Debug)]
pub struct AccelerometerData {}
pub struct GyroscopeData {}
pub struct CompassData {}

#[derive(Debug)]
pub struct ImuData {
    accelerometer: Option<AccelerometerData>,
}
