class Appender:
    def __init__(self, filename):
        self.filename = filename
        self.f = open(self.filename, 'at')

    def close(self):
        self.f.close()

    def write(self, item):
        self.f.write(item)
        self.f.write("\n")
