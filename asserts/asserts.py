"""
This file contains custom Exception types that might be raised during the operation of the boat.
"""

class CriticalError(Exception):
    """
    A critical error is an error that requires the boat to be stopped and the pilot to evacuate the
    boat.
    """

    def __init__(self, msg=None):
        if msg is not None:
            # Add any error message for more precice error messages
            super().__init__(self, "Critical error, shutting down: {msg}")
        else:
            super().__init__(self, "Critical error, shutting down.")


class WarningError(Exception):
    """
    A warning error is an error that requires the pilot to check the status as well as the onshore
    team, and take appropriate action.
    """

    def __init__(self, msg=None):
        if msg is not None:
            # Add any error message for more precice error messages
            super().__init__(
                self, "Warning, check sensors and component temperatures: {msg}"
            )
        else:
            super().__init__(self, "Warning, check sensors and component temperatures.")


class StartUpError(Exception):
    """
    A startup error is an error that occurs during the startup procedure, making impossible to
    safely start the boat. This can be linked to pressure issues, fuel cell issues, etc.
    """

    def __init__(self):
        super().__init__(self, "Startup error, check cells, valves and manometers.")


class ShutDownError(Exception):
    """
    A shutdown error is an error that occurs during the shutdown procedure, where the boat could
    not complete the shutdown procedure due to unresponsive components or fuel cell issues.
    """

    def __init__(self):
        super().__init__(self, "Shutdown error, check cells, valves and manometers.")
