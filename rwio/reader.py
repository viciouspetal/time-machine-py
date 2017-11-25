class Reader:
    def __init__(self, filename):
        self.filename = filename
        self.f = open(self.filename, 'rt')

    def close(self):
        self.f.close()

    def read(self):
        return self.f.readlines()

    def list_content(self):
        lines = self.read()

        for line in lines:
            print(line, sep="\n", end="\n")
        self.close()
