use crate::devices::{Exception, Name};

/// Message struct to be sent from devices in case of an exception
pub struct Message {
    name: Name,
    exception: Exception,
}

impl Message {
    pub fn new(name: Name, exception: Exception) -> Message {
        Message { name, exception }
    }

    pub fn get_name(&self) -> Name {
        self.name
    }

    pub fn get_exception(&self) -> Exception {
        self.exception
    }
}

// TODO: implement ordering for messages
