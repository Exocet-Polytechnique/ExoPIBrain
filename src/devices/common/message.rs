use std::time::Duration;

use crate::devices::{Exception, Name};

/// Message struct to be sent from devices in case of an exception
pub struct Message {
    name: Name,
    exception: Exception,
    timeout_duration: Option<Duration>,
}

impl Message {
    pub fn new(name: Name, exception: Exception) -> Message {
        Message {
            name,
            exception,
            timeout_duration: None,
        }
    }

    pub fn timeout(self, duration: Duration) -> Self {
        Message {
            timeout_duration: Some(duration),
            ..self
        }
    }

    pub fn get_name(&self) -> Name {
        self.name
    }

    pub fn get_exception(&self) -> Exception {
        self.exception
    }

    pub fn get_timeout_duration(&self) -> Option<Duration> {
        self.timeout_duration
    }
}

// TODO: implement ordering for messages
