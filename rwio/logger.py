from rwio.writer import Writer


class Logger:
    def __init__(self):
        self.logfile = "timemachine.log"

    def log(self, item):
        print(item)
        log = Writer("timemachine.log")
        log.write(item)
        log.close()
