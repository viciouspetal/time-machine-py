from rwio.appender import Appender


class Logger:
    def __init__(self):
        self.logfile = "timemachine.log"

    def log(self, item):
        print(item)
        log = Appender("timemachine.log")
        log.write(item)
        log.close()
