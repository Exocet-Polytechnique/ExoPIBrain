from sensors.temperature import Thermocouples
from sensors.pressure import Manometers
from config import CONFIG

def main():
    """Shows the temperature and pressure"""
    temperature = Thermocouples(None, None, None, CONFIG["TEMPERATURES"])
    pressure = Manometers(None, None, None, CONFIG["MANOMETERS"])
    while True:
        temp_data = temperature.read_raw_data()
        pressure_data = pressure.read_raw_data()
        print("Plaque H2 (°C):", temp_data["H2_plate"])
        print("Refuelling station (°C):", temp_data["refuelling_station"])
        print("Flottant (°C):", temp_data["floating"])
        print("Haute pression (bar):", pressure_data["high_pressure"])
        print("Basse pression (bar):", pressure_data["low_pressure"])
        print("\n\n\n\n\n")

if __name__ == "__main__":
    main()
