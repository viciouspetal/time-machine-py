import argparse
import datetime
import os
from shutil import copy2

from rwio.logger import Logger
from rwio.reader import Reader
from rwio.remover import Remover
from rwio.writer import Writer


def print_last_mod_date(filename):
    timestamp = os.path.getmtime(filename)
    print(filename, " ", timestamp)
    print(filename, " ", datetime.datetime.fromtimestamp(timestamp))


def get_timestamp_for_file(filename):
    return os.path.getmtime(filename)


def get_last_modified_date(args):
    # get list of watched files
    r1 = Reader(args.config)
    file_paths = r1.read()
    log1 = Logger()

    # determine if any of the watched files have changed
    for filepath in file_paths:
        # first, get current & previous timestamp
        current_timestamp = get_timestamp_for_file(filepath.replace("\n", ""))
        prev_timestamp = get_previous_timestamp()

        # determine if backup is necessary
        if current_timestamp > prev_timestamp:
            # create destination path and backup file
            destination = os.path.join(args.destinationPath, "backups")
            log1.log("Copying: " + filepath.replace("\n", "") + " to " + destination)
            copy_file(filepath, destination)


def get_previous_timestamp():
    return 0


def copy_file(filename, destination):
    copy2(filename, destination)


def backup_files(args):
    get_last_modified_date(args)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", default='config.dat')
    parser.add_argument("--destinationPath", default='.')
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--remove")
    parser.add_argument("--add")

    args = parser.parse_args()

    if args.list:
        print(args)
    elif args.remove:
        remove_file(args)
    elif args.add:
        add_file(args)
    else:
        backup_files(args)


def remove_file(args):
    log1 = Logger()
    remover1 = Remover(args.config)
    log1.log("Removing " + args.remove + " from list of watched files: " + args.config)
    remover1.remove(args.remove)


def add_file(args):
    log1 = Logger()
    w1 = Writer(args.config)
    log1.log("Adding " + args.add + " to list of watched files: " + args.config)
    w1.write(args.add)


if __name__ == "__main__":
    main()
