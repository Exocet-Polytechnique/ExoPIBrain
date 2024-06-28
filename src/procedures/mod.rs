pub mod precharge;
pub mod startup;

pub enum Error {
    StartUp(String),
    ShutDown(String),
    Critical(String),
    Warning(String),
}
