from multithreading.stream_reader import StreamReader
import re
import serial
from serial.serialutil import SerialException

READ_INTERVAL = 1
class FuelCell(StreamReader):
    def __init__(self, priority, lock, queue, read_interval, with_checks, serial_port):
        super().__init__(priority, lock, queue, read_interval, with_checks)
        self.serial_port = serial_port
        self.ser = serial.Serial(self.serial_port)  # Open port with baud rate
        units = ["V", "C", "B", "A", "W", "Wh"]
        self.regexp = re.compile(r'(\d+)\s*(%s)\b' % '|'.join(units))

    def read_raw_data(self):
        fuel_cell_data = {}
        try:
            #received_data = (str)(self.ser.readline())
            # Example from the documentation:
            received_data = "|FC_V : 71.17 V |   FCT1:  30.90 C   |   H2P1  :  0.61 B |   DCDCV: 30.5 V   |FC_A  : 10.21 A |   FCT2:  28.46 C   |   H2P2  :  0.59 B |   DCDCA: 12.8 A   |FC_W  : 726.6 W |   FAN :    89 %    |   Tank-P: 117.0 B |   DCDCW: 1234.5 W |Energy:   298 Wh|   BLW :    21 %    |   Tank-T: 25.08 C |   BattV:  23.49 V ||                    |                   |                   !"
            received_data = re.sub(self.regexp, r'\1', received_data.replace(" ", "")).split("|")
            for d in received_data:
                if d != "" and d != "!":
                    measure, value = d.split(":")
                    if value[-1] == "%":
                        value = float(value[:-1]) / 100
                    value = float(value)
                    fuel_cell_data[measure] = value

        except SerialException:
            print(f"Fuel cell {self.serial_port} fucked")
        
        return 'FuelCell', fuel_cell_data