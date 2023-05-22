from multithreading.stream_reader import StreamReader
import re
import time
import serial
from serial.serialutil import SerialException

ANODE_SUPPLY_PRESSURE_OK = "Anode Supply Pressure OK"
TEMPERATURE_OK = "Temperature Check OK"
SYSTEM_OFF = "System Off"

regexp = re.compile(r'(\d+)\s*(%s)\b' % '|'.join(["V", "C", "B", "A", "W", "Wh"]))
class FuelCell(StreamReader):
    def __init__(self, lock, data_queue, log_queue, config):
        super().__init__(lock, data_queue, log_queue, config)
        self.serial_port = config['serial_port']
        self.ser = serial.Serial(self.serial_port, 57600)  # Open port with baud rate
        self.started = False
    
    def write(self, command_str):
        self.ser.write(command_str)
        self.ser.write(b"\r")

    def start_fuel_cell(self):
        self.write("start")
        temp_ok = False
        pressure_ok = False
        while not temp_ok or not pressure_ok:
            if self.ser.in_waiting > 0:
                received_data = self.ser.readline()
                if ANODE_SUPPLY_PRESSURE_OK in received_data:
                    pressure_ok = True
                if TEMPERATURE_OK in received_data:
                    temp_ok = True
            time.sleep(0.2)
        self.started = True
        
    def shutdown_fuel_cell(self):
        self.write("end")
        system_off = False
        while not system_off:
            if self.ser.in_waiting > 0:
                received_data = self.ser.readline()
                if SYSTEM_OFF in received_data:
                    system_off = True
            time.sleep(0.2)
        self.started = False

    def read_raw_data(self):
        fuel_cell_data = {}
        try:
            #received_data = (str)(self.ser.readline())
            # Example from the documentation:
            received_data = "|FC_V : 71.17 V |   FCT1:  30.90 C   |   H2P1  :  0.61 B |   DCDCV: 30.5 V   |FC_A  : 10.21 A |   FCT2:  28.46 C   |   H2P2  :  0.59 B |   DCDCA: 12.8 A   |FC_W  : 726.6 W |   FAN :    89 %    |   Tank-P: 117.0 B |   DCDCW: 1234.5 W |Energy:   298 Wh|   BLW :    21 %    |   Tank-T: 25.08 C |   BattV:  23.49 V ||                    |                   |                   !"
            received_data = re.sub(regexp, r'\1', received_data.replace(" ", "")).split("|")
            for d in received_data:
                if d == "!":
                    break
                if d != "":
                    measure, value = d.split(":")
                    if value[-1] == "%":
                        value = float(value[:-1]) / 100
                    value = float(value)
                    fuel_cell_data[measure] = value

        except SerialException:
            print(f"Fuel cell {self.serial_port} fucked")
        
        return fuel_cell_data
    