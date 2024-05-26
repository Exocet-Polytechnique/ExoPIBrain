use std::sync::Arc;

struct LoopingThread<T> {
    function: T,
    stop_signal: Arc<bool>,
}

impl<T> LoopingThread<T>
where
    T: FnMut() -> (),
{
    pub fn new(function: T, stop_signal: &Arc<bool>) -> LoopingThread<T> {
        LoopingThread {
            function,
            stop_signal: stop_signal.clone(),
        }
    }

    pub fn start(&mut self) -> () {
        loop {
            if *self.stop_signal {
                break;
            }
            (self.function)();
        }
    }
}
