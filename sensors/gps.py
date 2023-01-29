from gps3 import gps3
from data_readers.stream_reader import StreamReader

class GPS(StreamReader):
    def __init__(self) -> None:
        self.gps_socket = gps3.GPSDSocket()
        self.data_stream = gps3.DataStream()
        self.gps_socket.connect()
        self.gps_socket.watch()

    def read(self):
        for data in self.gps_socket:
            if data:
                self.data_stream.unpack(data)
                print('Altitude = ', self.data_stream.TPV['alt'])
                print('Latitude = ', self.data_stream.TPV['lat'])

