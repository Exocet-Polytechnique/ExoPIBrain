from sensors.gps import GPS
from time import sleep
if __name__ == "__main__":
    gps = GPS()
    while True:
        res = gps.read(with_checks=False)
        print(res)
