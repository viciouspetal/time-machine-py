import argparse
import datetime
import hashlib
import os
from shutil import copy2

from rwio.appender import Appender
from rwio.logger import Logger
from rwio.reader import Reader
from rwio.remover import Remover
from rwio.writer import Writer


def get_timestamp_for_file(filename):
    return os.path.getmtime(filename)


def get_folder_name_hash(path):
    hashed_folder = hashlib.md5(path.encode('UTF-8'))
    return hashed_folder.hexdigest()


def check_if_folder_exists_and_create(path):
    if not os.path.exists(path):
        Logger().log("Creating folder: " + path)
        os.makedirs(path)


def get_previous_timestamp(destination_root, filepath_hash):
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


def copy_file(filename, destination):
    copy2(filename, destination)


def backup_files(args):
    # get list of watched files
    r1 = Reader(args.config)
    file_paths = r1.read()
    r1.close()
    log1 = Logger()
    found_eligible_files_for_backup = False

    # determine if any of the watched files have changed
    for filepath in file_paths:
        # first, get current & previous timestamp
        filepath = clean_path(filepath)

        # create destination path and backup file
        filepath_hash = get_folder_name_hash(filepath)
        destination_root = os.path.join(args.destinationPath, "backups")
        destination = os.path.join(destination_root, filepath_hash)

        # determine if backup is necessary
        if is_backup_needed(filepath, destination_root, filepath_hash):
            found_eligible_files_for_backup = True
            check_if_folder_exists_and_create(destination)

            # update last modified date of backed up file to determine need to execute backup when script is run next
            save_timestamp(destination, filepath_hash, get_timestamp_for_file(filepath))

            log1.log("Copying: " + filepath + " to " + destination)
            copy_file(filepath, destination)
    if not found_eligible_files_for_backup:
        log1.log("No files eligible for backup were found")


def save_timestamp(path, filename, timestamp):
    filepath = os.path.join(path, filename)
    w1 = Writer(filepath)
    Logger().log("Saving last modified date of: " + str(timestamp) + " in " + filepath)
    w1.write(str(timestamp))
    w1.close()


def clean_path(path):
    return path.replace("\n", "")


def is_backup_needed(filepath, destination_root, filepath_hash):
    current_timestamp = get_timestamp_for_file(filepath)
    prev_timestamp = get_previous_timestamp(destination_root, filepath_hash)

    return current_timestamp > prev_timestamp


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", default='config.dat')
    parser.add_argument("--destinationPath", default='.')
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--remove")
    parser.add_argument("--add")

    args = parser.parse_args()

    if args.list:
        list_config_contents(args.config)
    elif args.remove:
        remove_file(args)
    elif args.add:
        add_file(args)
    else:
        backup_files(args)


def remove_file(args):
    log1 = Logger()
    if not os.path.exists(args.remove):
        log1.log("Attempting to remove " + args.remove + " from " + args.config + " failed.")
        log1.log("File could not be located. Ensure the file exists before proceeding")
    else:
        remover1 = Remover(args.config)
        log1.log("Removing " + args.remove + " from list of watched files: " + args.config)
        remover1.remove(args.remove)


def add_file(args):
    log1 = Logger()
    if not os.path.exists(args.add):
        log1.log("Attempting to add " + args.add + " to " + args.config + " failed.")
        log1.log("File could not be located. Ensure the file exists before proceeding")
    else:
        w1 = Appender(args.config)
        log1.log("Adding " + args.add + " to list of watched files: " + args.config)
        w1.write(args.add)


def list_config_contents(config_path):
    if os.path.exists(config_path):
        print("Currently watching the following files:")
        r1 = Reader(config_path)
        r1.print_content()
        r1.close()
    else:
        Logger().log("Couldn't locate: " + config_path)
        Logger().log("Ensure the file exists before proceeding.")


if __name__ == "__main__":
    main()
