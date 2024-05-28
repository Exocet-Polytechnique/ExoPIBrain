pub mod precharge;

pub enum Error {
    StartUp(String),
    ShutDown(String),
    Critical(String),
    Warning(String),
}
