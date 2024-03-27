"""
Result class for sensor readings, inspired by Rust's Result type. It can hold
either a valid value or an error and a message.
"""

class SensorResult:
    """SensorResult type that can contain either a value or a reason why there isn't any."""

    def __init__(self, is_valid, value):
        """
        The second parameter of this constructor can be either valid sensor data or an error
        message id (see messages.py).
        """

        self.is_valid_ = is_valid

        if self.is_valid_:
            # value can contain anything and will be publicaly accessible
            self.value = value
        else:
            # in this case, the second parameter passed to the constructor
            # will be the error message id
            self.error_message_id_ = value

    def is_valid(self):
        """Returns the state of the result."""

        return self.is_valid_

    def get_error_message_id_(self):
        """Returns the error message."""

        if not self.is_valid_:
            return self.error_message_id_

        return None
