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
        self.course_angle = 0

    def _convert_to_degrees(self, raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" % position
        return position

    def read_raw_data(self):
        try:
            received_data = (str)(self.ser.readline())
            gprmc_data_available = received_data.find("$GPRMC,")   #check for NMEA GPGGA string    
            if (gprmc_data_available > 0):
                sentence = received_data.split("$GPRMC,", 1)[1]
                nmea_buff = sentence.split(",")
                self.nmea_time = float(nmea_buff[0])
                self.speed_knots = float(nmea_buff[6])
                self.course_angle = 0.0 if nmea_buff[7] == '' else float(nmea_buff[7])
                self.lat_deg = self._convert_to_degrees(float(nmea_buff[2]))
                self.long_deg = self._convert_to_degrees(float(nmea_buff[4]))
        except SerialException:
            print("GPS fucked")

        return {"nmea_time": self.nmea_time, "speed_knots": self.speed_knots, "course_angle": self.course_angle, "lat_deg": self.lat_deg, "long_deg": self.long_deg}

