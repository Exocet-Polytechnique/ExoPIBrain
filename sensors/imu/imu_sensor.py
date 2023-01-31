class IMUSensor:
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def read(self):
        raise NotImplementedError()