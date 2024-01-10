class SensorError(Exception):
    """Base class for all sensor errors"""
    pass

class ConnectionError(SensorError):
    """No connection to the sensor"""
    pass 

class InvalidDataError(SensorError):
    """The data received by the sensor is corrupt or invalid"""
    pass