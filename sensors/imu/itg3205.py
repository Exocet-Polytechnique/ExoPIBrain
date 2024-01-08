from imu_sensor import IMUSensor


class ITG3205(IMUSensor):
    """
    https://github.com/ControlEverythingCommunity/ITG3200/blob/master/Python/ITG_3200.py
    """
    POWER_MANAGEMENT = 0x3E
    PLL_X_GYRO = 0x01
    DLPF_FS = 0x16
    DLPF_256_8 = 0x18
    DATA_REG = 0x1D

    def __init__(self, bus):
        super().__init__(bus, address=0x68)
        self.write_byte(self.POWER_MANAGEMENT, self.PLL_X_GYRO)
        self.write_byte(self.DLPF_FS, self.DLPF_256_8)

    def read(self):
        data = self.read_block(self.DATA_REG, 6)
        # Convert the data
        x_gyro = data[0] * 256 + data[1]
        if x_gyro > 32767 :
            x_gyro -= 65536

        y_gyro = data[2] * 256 + data[3]
        if y_gyro > 32767 :
            y_gyro -= 65536

        z_gyro = data[4] * 256 + data[5]
        if z_gyro > 32767 :
            z_gyro -= 65536
        
        return x_gyro, y_gyro, z_gyro
