class StreamReader:
    def read_data(self, *args, **kwargs):
        return None

    def alert(self, *args, **kwargs):
        raise NotImplementedError()
    
    def read_check(self, *args, **kwargs):
        data = self.read_data(*args, **kwargs)
        self.alert(data)
        return data
