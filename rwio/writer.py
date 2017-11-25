class Writer:
    def __init__(self, filename):
        self.filename = filename
        self.f = open(self.filename, 'wt')

    def close(self):
        self.f.close()

    def write(self, item):
        return self.f.write(item)
