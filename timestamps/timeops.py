import os

from rwio.logger import Logger
from rwio.reader import Reader
from rwio.writer import Writer
from utils.pathutils import Pathutils


class Timeops:
    def get_timestamp_for_file(self, filename):
        clean_filename = Pathutils().clean_path(filename)
        return os.path.getmtime(clean_filename)

    def save_timestamp(self, path, filename, timestamp):
        filepath = os.path.join(path, filename)
        w1 = Writer(filepath)
        Logger().log("Saving last modified date of: " + str(timestamp) + " in " + filepath)
        w1.write(str(timestamp))
        w1.close()

    def get_previous_timestamp(self, destination_root, filepath_hash):
        timestamp_file_path = os.path.join(destination_root, filepath_hash, filepath_hash)

        if not os.path.exists(timestamp_file_path):
            return 0.0
        else:
            r1 = Reader(timestamp_file_path)
            prev_timestamps = r1.read()
            r1.close()
            if len(prev_timestamps) <= 0:
                return 0.0
            else:
                return float(prev_timestamps[0])
