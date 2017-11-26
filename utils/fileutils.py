import hashlib
import os
from shutil import copy2

from rwio.logger import Logger
from utils.pathutils import Pathutils


class Fileutils:
    def get_folder_name_hash(self, path):
        clean_path = Pathutils().clean_path(path)
        hashed_folder = hashlib.md5(clean_path.encode('UTF-8'))
        return hashed_folder.hexdigest()

    def check_if_folder_exists_and_create(self, path):
        clean_path = Pathutils().clean_path(path)
        if not os.path.exists(clean_path):
            Logger().log("Creating folder: " + path)
            os.makedirs(path)

    def copy_file(self, source_filepath, args, current_timestamp):
        # generate backup path
        destination_root = self.generate_backup_filepath(args, source_filepath)
        backup_destination = os.path.join(destination_root, str(current_timestamp))

        # ensure that target directory structure exists and if not create it
        self.check_if_folder_exists_and_create(backup_destination)

        # log operation and perform backup
        clean_filename = Pathutils().clean_path(source_filepath)
        Logger().log("Copying: " + source_filepath + " to " + backup_destination)
        copy2(clean_filename, backup_destination)

    def check_exists(self, filename):
        if not os.path.exists(filename):
            Logger().log("File: \"" + filename + "\" could not be found. Ensure the file exists before proceeding")
            return False
        else:
            return True

    def generate_backup_filepath(self, args, filepath):
        filepath_hash = self.get_folder_name_hash(filepath)
        destination_root = os.path.join(args.destinationPath)
        return os.path.join(destination_root, filepath_hash)
