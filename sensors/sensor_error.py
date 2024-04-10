class SensorError(Exception):
    """Base class for all sensor errors"""
    pass

class SensorConnectionError(SensorError):
    """No connection to the sensor"""
    pass 

class InvalidDataError(SensorError):
    """The data received by the sensor is corrupt or invalid"""
    pass

class SensorException(SensorError):
    """Generic sensor exception. Allows for sending message ids."""
    def __init__(self, exception_id):
        self.exception_id = exception_id
