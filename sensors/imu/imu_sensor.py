import time 

class IMUSensor:
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def read(self):
        raise NotImplementedError()

    def write_byte(self, register, value):
        self.bus.write_byte_data(self.address, register, value)
        time.sleep(0.01)

    def read_byte(self, register):
        return self.bus.read_byte_data(self.address, register)