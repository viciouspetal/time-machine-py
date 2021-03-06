from rwio.writer import Writer


class Remover:
    def __init__(self, filename):
        self.filename = filename

    def remove(self, item):
        r = open(self.filename, 'rt')
        lines = r.readlines()
        r.close()

        w = Writer(self.filename)
        for line in lines:
            if not line.endswith(item + "\n"):
                w.write(line)
        w.close()
