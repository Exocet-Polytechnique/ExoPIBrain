import serial
from serial.serialutil import SerialException
from data_readers.stream_reader import StreamReader

class GPS(StreamReader):
    '''
    GPS Interfacing with Raspberry Pi using Pyhton
    http://www.electronicwings.com
    '''

    def __init__(self) -> None:
        self.ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
        self.lat_deg = 0
        self.long_deg = 0
        self.nmea_time = 0
        self.speed_knots = 0

    def _convert_to_degrees(self, raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" % position
        return position

    def _read_raw_data(self):
        try:
            received_data = (str)(self.ser.readline())
            gpgga_data_available = received_data.find("$GPGGA,")   #check for NMEA GPGGA string    
            if (gpgga_data_available > 0):
                gpgga_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                nmea_buff = gpgga_buffer.split(",")

                self.nmea_time = nmea_buff[0]
                self.lat_deg = self._convert_to_degrees(float(nmea_buff[1]))
                self.long_deg = self._convert_to_degrees(float(nmea_buff[3]))
        except SerialException:
            pass

        return self.lat_deg, self.long_deg, self.nmea_time, self.speed_knots

