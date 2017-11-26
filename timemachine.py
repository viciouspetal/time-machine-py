import argparse
import os

from rwio.logger import Logger
from rwio.reader import Reader
from rwio.writer import Writer
from timestamps.timeops import Timeops
from utils.argutils import Argutils
from utils.fileutils import Fileutils


def backup_files(args):
    # get list of watched files
    r1 = Reader(args.config)
    file_paths = r1.read()
    r1.close()
    log1 = Logger()
    found_eligible_files_for_backup = False

    # determine if any of the watched files have changed
    for filepath in file_paths:
        file_utils = Fileutils()

        # create destination path and backup file
        # TODO this needs to get kicked to fileutils!
        filepath_hash = file_utils.get_folder_name_hash(filepath)
        destination_root = os.path.join(args.destinationPath, "backups")
        destination = file_utils.generate_backup_filepath(args, filepath)

        # determine if backup is necessary
        if is_backup_needed(filepath, destination_root, filepath_hash):
            found_eligible_files_for_backup = True
            file_utils.check_if_folder_exists_and_create(destination)
            timeops = Timeops()

            # update last modified date of backed up file to determine need to execute backup when script is run next
            timeops.save_timestamp(destination, filepath_hash, timeops.get_timestamp_for_file(filepath))

            log1.log("Copying: " + filepath + " to " + destination)
            file_utils.copy_file(filepath, destination)
    if not found_eligible_files_for_backup:
        log1.log("No files eligible for backup were found")


def is_backup_needed(filepath, destination_root, filepath_hash):
    timeops = Timeops()
    current_timestamp = timeops.get_timestamp_for_file(filepath)
    prev_timestamp = timeops.get_previous_timestamp(destination_root, filepath_hash)

    return current_timestamp > prev_timestamp

def create_default_config(default_config_path):
    w1 = Writer(default_config_path)
    w1.write("")
    w1.close()

def main():
    parser = argparse.ArgumentParser()
    default_config = 'config.dat'
    parser.add_argument("--config", default=default_config)
    parser.add_argument("--destinationPath", default='.')
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--remove")
    parser.add_argument("--add")

    args = parser.parse_args()
    arg_utils = Argutils()

    if not os.path.exists(default_config):
        create_default_config(default_config)

    if args.list:
        arg_utils.print_config_contents(args.config)
    elif args.remove:
        arg_utils.remove_file(args)
    elif args.add:
        arg_utils.add_file(args)
    else:
        backup_files(args)


if __name__ == "__main__":
    main()
