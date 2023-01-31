class StreamReader:
    def read_raw_data(self, *args, **kwargs):
        return 0

    def alert(self, *args, **kwargs):
        raise NotImplementedError()
    
    def read(self, *args, with_checks=True, **kwargs):
        data = self.read_raw_data(*args, **kwargs)
        if with_checks:
            self.alert(data)
        return data
