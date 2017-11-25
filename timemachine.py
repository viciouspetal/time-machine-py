import argparse
import datetime
import os

import rwio.reader


def print_last_mod_date(filename):
    timestamp = os.path.getmtime(filename)
    print(timestamp)
    print(datetime.datetime.fromtimestamp(timestamp))

def get_last_modified_date(config):
    # get list of contents
    r1 = rwio.reader.Reader(config)
    lines = r1.read()
    print(lines)

def backup_files(args):
    get_last_modified_date(args.config)

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
