#[derive(Debug)]
pub enum DeviceException {
    NotConnected,
}

impl From<rppal::i2c::Error> for DeviceException {
    fn from(value: rppal::i2c::Error) -> Self {
        DeviceException::NotConnected
    }
}
