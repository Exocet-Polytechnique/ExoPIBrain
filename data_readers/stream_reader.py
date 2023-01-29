class StreamReader:
    def _read_raw_data(self, *args, **kwargs):
        return 0

    def _alert(self, *args, **kwargs):
        raise NotImplementedError()
    
    def read(self, *args, with_checks=True, **kwargs):
        data = self._read_raw_data(*args, **kwargs)
        if with_checks:
            self._alert(data)
        return data
