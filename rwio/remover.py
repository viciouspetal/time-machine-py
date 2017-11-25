class Remover:
    def __init__(self, filename):
        self.filename = filename

    def remove(self, item):
        r = open(self.filename, 'rt')
        lines = r.readlines()
        r.close()

        w = open(self.filename, 'wt')
        # TODO need to find out why os.linesep function was not working
        for line in lines:
            if not line.endswith(item + "\n"):
                w.write(line)
        w.close()
