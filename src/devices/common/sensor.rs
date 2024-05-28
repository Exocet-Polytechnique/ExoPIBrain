pub trait Sensor<T> {
    async fn read(&self) -> Option<T>;
    fn is_connected(&self) -> bool;
    fn shutdown(&mut self);
    fn initialize(&mut self);
}
