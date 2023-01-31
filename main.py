from sensors.gps import GPS
import smbus
from sensors.imu.hmc5883l import QMC5883l
from time import sleep

if __name__ == "__main__":
    gps = GPS()
    bus = smbus.SMBus(1)
    sleep(1)
    sns = QMC5883l(bus)  # ADXL345(bus)
    while True:
        # res = gps.read(with_checks=False)
        res = sns.get_data()
        print(res)
        sleep(1)
