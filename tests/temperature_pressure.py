from sensors.temperature import Thermocouples
# from sensors.pressure import Manometers
from config import CONFIG

def main():
    """Shows the temperature and pressure"""
    temperature = Thermocouples(None, None, None, CONFIG["TEMPERATURES"])
    while True:
        print(temperature.read_raw_data())

if __name__ == "__main__":
    main()
