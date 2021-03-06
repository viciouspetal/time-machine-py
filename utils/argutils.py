import os

from rwio.appender import Appender
from rwio.logger import Logger
from rwio.reader import Reader
from rwio.remover import Remover
from utils.fileutils import Fileutils


class Argutils:
    def remove_file(self, args):
        log1 = Logger()
        if not os.path.exists(args.config):
            log1.log("Attempting to remove " + args.remove + " from " + args.config + " failed.")
            log1.log("Config file could not be located. Ensure the file exists before proceeding")
        else:
            remover1 = Remover(args.config)
            log1.log("Removing " + args.remove + " from list of watched files: " + args.config)
            remover1.remove(args.remove)

    def add_file(self, args):
        log1 = Logger()
        if not os.path.exists(args.add):
            log1.log("Attempting to add " + args.add + " to " + args.config + " failed")
            log1.log("File could not be located. Ensure the file exists before proceeding")
        elif self.is_duplicate_addition(args.config, args.add):
            log1.log(args.add + " is already watched nad was not added again")
        else:
            w1 = Appender(args.config)
            log1.log("Adding " + args.add + " to list of watched files: " + args.config)
            w1.write(args.add)
            log1.log("Taking initial backup of: " + args.add)
            Fileutils().copy_file(args.add, args, 0)

    def print_config_contents(self, config_path):
        if os.path.exists(config_path):
            print("Currently watching the following files:")
            r1 = Reader(config_path)
            r1.print_content()
            r1.close()
        else:
            Logger().log("Could not locate: " + config_path + "Ensure the file exists before proceeding")

    def is_duplicate_addition(self, filename, item_to_be_added):
        r1 = Reader(filename)
        lines = r1.read()

        for line in lines:
            if line == item_to_be_added:
                return True
        return False
