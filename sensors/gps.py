import serial
from serial.serialutil import SerialException
from multithreading.stream_reader import StreamReader

READ_INTERVAL = 1
class GPS(StreamReader):
    """
    GPS Interfacing with Raspberry Pi using Python
    http://www.electronicwings.com
    """

    def __init__(self, priority, lock, queue, serial_port="/dev/ttyS0") -> None:
        super().__init__(priority, lock, queue, READ_INTERVAL, False)
        self.serial_port = serial_port
        self.ser = serial.Serial(self.serial_port)  # Open port with baud rate

    def _convert_to_degrees(self, raw_value):
        decimal_value = raw_value / 100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
        position = degrees + mm_mmmm
        position = "%.4f" % position
        return position

    def read_raw_data(self):
        gps_data = {}
        try:
            received_data = (str)(self.ser.readline())
            gprmc_data_available = received_data.find(
                "$GPRMC,"
            )  # check for NMEA GPGGA string
            if gprmc_data_available > 0:
                sentence = received_data.split("$GPRMC,", 1)[1]
                nmea_buff = sentence.split(",")
                gps_data["nmea_time"] = float(nmea_buff[0])
                gps_data["speed_knots"] = float(nmea_buff[6])
                gps_data["course_angle"] = 0.0 if nmea_buff[7] == "" else float(nmea_buff[7])
                gps_data["lat_deg"] = self._convert_to_degrees(float(nmea_buff[2]))
                gps_data["long_deg"] = self._convert_to_degrees(float(nmea_buff[4])) * -1
        except SerialException:
            print("GPS fucked")

        return 'GPS', gps_data
