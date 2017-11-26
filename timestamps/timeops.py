import os

from rwio.logger import Logger
from rwio.reader import Reader
from rwio.writer import Writer
from utils.fileutils import Fileutils
from utils.pathutils import Pathutils


class Timeops:
    def get_timestamp_for_file(self, filename):
        clean_filename = Pathutils().clean_path(filename)
        if Fileutils().check_exists(clean_filename):
            return os.path.getmtime(clean_filename)
        else:
            return 0.0

    def save_timestamp(self, args, source_filepath):
        file_utils = Fileutils()
        # prepare paths, and aggregate values to be saved
        source_file_hash = file_utils.get_folder_name_hash(source_filepath)
        timestamp_destination = file_utils.generate_backup_filepath(args, source_filepath)
        current_timestamp = self.get_timestamp_for_file(source_filepath)

        # check target timestamp folder exists - and if it doesn't create it
        file_utils.check_if_folder_exists_and_create(timestamp_destination)

        # save timestamp
        filepath = os.path.join(timestamp_destination, source_file_hash)
        w1 = Writer(filepath)
        Logger().log("Saving last modified date of: " + source_filepath + " in " + filepath)
        w1.write(str(current_timestamp))
        w1.close()

    def get_previous_timestamp(self, args, filepath_hash):

        timestamp_file_path = os.path.join(args.destinationPath, filepath_hash, filepath_hash)

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
