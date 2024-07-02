use std::{cmp::Ordering, time::Duration};

use crate::devices::{Exception, Name};

/// Message struct to be sent from devices in case of an exception
#[derive(PartialEq, Eq, Clone)]
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

    pub fn to_string(&self) -> String {
        format!("{:?}: {:?}", self.name, self.exception)
    }

    pub fn is_critical(&self) -> bool {
        self.exception <= Exception::CriticalError
    }
}

impl PartialOrd for Message {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Message {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.exception.cmp(&other.exception) != Ordering::Equal {
            self.name.cmp(&other.name)
        } else {
            self.exception.cmp(&other.exception)
        }
    }
}
