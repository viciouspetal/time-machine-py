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
    for source_filepath in file_paths:
        file_utils = Fileutils()

        # create destination path and backup file
        source_filepath_hash = file_utils.get_folder_name_hash(source_filepath)

        # determine if backup is necessary
        if is_backup_needed(source_filepath, args, source_filepath_hash):
            timeops = Timeops()
            found_eligible_files_for_backup = True

            current_timestamp = timeops.get_timestamp_for_file(source_filepath)
            # backup_destination = os.path.join(timestamp_destination, str(current_timestamp))

            # update last modified date of backed up file to determine need to execute backup when script is run next
            timeops.save_timestamp(args, source_filepath)

            file_utils.copy_file(source_filepath, args, current_timestamp)
    if not found_eligible_files_for_backup:
        log1.log("No files eligible for backup were found")


def is_backup_needed(source_filepath, args, filepath_hash):
    timeops = Timeops()
    current_timestamp = timeops.get_timestamp_for_file(source_filepath)
    prev_timestamp = timeops.get_previous_timestamp(args, filepath_hash)

    return current_timestamp > prev_timestamp


def create_default_config(default_config_path):
    w1 = Writer(default_config_path)
    w1.write("")
    w1.close()


def main():
    default_config = 'config.dat'
    # define allowed arguments and initalize their default values, when applicable
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=default_config)
    parser.add_argument("--destinationPath", default='.')
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--remove")
    parser.add_argument("--add")

    args = parser.parse_args()
    arg_utils = Argutils()

    # ensure that a config file exists at all times
    if not os.path.exists(default_config):
        create_default_config(default_config)

    # branch execution depending on the option selected
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
