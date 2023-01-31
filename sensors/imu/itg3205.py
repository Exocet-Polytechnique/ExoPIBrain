from imu_sensor import IMUSensor

class ITG3205(IMUSensor):
    """
    https://github.com/ControlEverythingCommunity/ITG3200/blob/master/Python/ITG_3200.py
    """
    def __init__(self, bus):
        super().__init__(bus, address=0x68)
    
    def read(self):
        # pitch, roll, yaw
        return 0,0,0
