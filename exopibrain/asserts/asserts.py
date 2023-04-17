IMU = {"alert": (40, 60), "critical": (60, float("inf"))}


class CriticalError(Exception):
    pass


class AlertError(Exception):
    pass
