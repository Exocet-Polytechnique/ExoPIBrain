from fuel_cell.actuators import Actuator
from config import CONFIG
import sys

def control_actuator(open1, open2):
    """
    Controls the actuators
    """
    actuator1 = Actuator(
        CONFIG["ACTUATORS"]["valve1"]["output_pin"],
        CONFIG["ACTUATORS"]["valve1"]["error_pin"],
        CONFIG["ACTUATORS"]["valve1"]["closed_on_low"])

    actuator2 = Actuator(
        CONFIG["ACTUATORS"]["valve2"]["output_pin"],
        CONFIG["ACTUATORS"]["valve2"]["error_pin"],
        CONFIG["ACTUATORS"]["valve2"]["closed_on_low"])

    if open1:
        actuator1.open_valve()
    else:
        actuator1.close_valve()

    if open2:
        actuator2.open_valve()
    else:
        actuator2.close_valve()

def main():
    """
    Parses arguments to control the actuators
    """
    args = sys.argv[1:]
    if len(args) != 2:
        print("Utilisation: ./valve_control <valve1> <valve2>")
        sys.exit(1)

    if args[0] == "0":
        open1 = False
    elif args[0] == "1":
        open1 = True
    else:
        print(
            "Usage: ./valve_control <valve1> <valve2>. <valve1> doit etre 0 (ferme) ou 1 (ouvert)")
        sys.exit(1)

    if args[1] == "0":
        open2 = False
    elif args[1] == "1":
        open2 = True
    else:
        print(
            "Usage: ./valve_control <valve1> <valve2>. <valve2> doit etre 0 (ferme) ou 1 (ouvert)")
        sys.exit(1)

    control_actuator(open1, open2)


if __name__ == "__main__":
    main()
