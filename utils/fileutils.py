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

    def copy_file(self, filename, destination):
        clean_filename = Pathutils().clean_path(filename)
        copy2(clean_filename, destination)
