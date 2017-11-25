import argparse
import datetime
import os
from shutil import copy2

from rwio.reader import Reader


def print_last_mod_date(filename):
    timestamp = os.path.getmtime(filename)
    print(filename, " ", timestamp)
    print(filename, " ", datetime.datetime.fromtimestamp(timestamp))


def get_timestamp_for_file(filename):
    return os.path.getmtime(filename)


def get_last_modified_date(args):
    # get list of files to be watched
    r1 = Reader(args.config)
    file_paths = r1.read()

    # determine if any of the watched files have changed
    # first, get current timestamps
    for filepath in file_paths:
        filename = os.path.split(filepath)[1]
        current_timestamp = get_timestamp_for_file(filepath.replace("\n", ""))
        prev_timestamp = 1511639730.8462887

        if current_timestamp > prev_timestamp:
            destination = os.path.join(args.storePath, "backups")
            print("Copying: " + filepath + " to " + destination)
            copy2(filepath, destination)


def copy_file(filename, destination):
    copy2(filename, destination)


def backup_files(args):
    get_last_modified_date(args)


def main(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", default='config.dat')
    parser.add_argument("--storePath", default='.')
    parser.add_argument("--list", action="store_true")

    args = parser.parse_args()

    if args.list:
        print(args)
    else:
        backup_files(args)


if __name__ == "__main__":
    main()
