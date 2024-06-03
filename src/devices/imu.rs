#[derive(Debug)]
pub struct AccelerometerData {}
#[derive(Debug)]
pub struct GyroscopeData {}
#[derive(Debug)]
pub struct CompassData {}

#[derive(Debug)]
pub struct ImuData {
    accelerometer: Option<AccelerometerData>,
}
