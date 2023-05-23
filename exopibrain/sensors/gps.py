from serial.serialutil import SerialException
from multithreading.stream_reader import SerialStreamReader

class GPS(SerialStreamReader):
    """
    GPS Interfacing with Raspberry Pi using Python
    http://www.electronicwings.com
    """

    def __init__(self, lock, data_queue, log_queue, config) -> None:
        """
        Args:
            lock (threading.Lock): The lock used to synchronize access to the queue.
            data_queue (queue.PriorityQueue): The queue to put the data in.
            log_queue (queue.Queue): The queue to put the data in.
            config (dict): The configuration for the sensor (serial port).
        """
        super().__init__(lock, data_queue, log_queue, config)

    def _convert_to_degrees(self, raw_value):
        """
        Converts raw gps value into decimal degrees

        Args:
            raw_value (float): The raw value from the GPS sensor.
        
        Returns:
            float: The converted value in decimal degrees.
        """
        decimal_value = raw_value / 100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
        position = degrees + mm_mmmm
        position = round(position, 5)
        return position

    def read_raw_data(self):
        """
        Reads the raw data from the GPS sensor.

        Returns:
            dict: The raw data from the GPS sensor.
        """
        gps_data = {}
        try:
            if self.ser.in_waiting:
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
            pass

        return gps_data
