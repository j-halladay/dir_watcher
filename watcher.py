#!/usr/bin/env python

import argparse
import signal
import logging
import os
import sys
import time
from datetime import datetime as dt

__author__ = "j_halladay"

logger = logging.getLogger(__name__)

watched_files = {}

signames = dict((k, v)
                for v, k in reversed(sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))

exit_flag = False


def directory_recorder(path, ext, magic_text):
    """records and updates directory files matching the extension"""
    global watched_files
    dirfiles = os.listdir(path)
    for file in dirfiles:
        if file.endswith(ext):
            if file not in watched_files:
                logger.info(
                    "File={} found, adding to watched list".format(file))
                watched_files[file] = 1
    for file in watched_files.keys():
        if file not in dirfiles:
            logger.info(
                "File={} removed, Removing from watched list".format(file))
            watched_files.pop(file)
    for f in watched_files:
        fullpath = os.path.join(path, f)
        startline = watched_files[f]
        watched_files[f] = scan_file(fullpath, startline, magic_text)


def scan_file(filename, startline, magic_text):
    """finds the magic text in a file"""
    with open(filename) as f:
        for line_num, line in enumerate(f):
            if line_num >= startline:
                if magic_text in line:
                    logger.info(
                        "Text ={} found in file={} at line={}".format(
                            magic_text,
                            filename, line_num+1))
    return line_num + 1


def signal_handler(sig_num, frame):
    """handles signals sent to the program"""

    logger.warn('Received ' + signames[sig_num])
    global exit_flag
    exit_flag = True


def create_parser():
    """Create a cmd line parser object"""
    parser = argparse.ArgumentParser()

    parser.add_argument('direct', help='directory to watch')
    parser.add_argument('mstring', help='string to find in text files')
    parser.add_argument("--interval", "-i",
                        help="amount of time between polls", type=float,
                        default=1.0)
    parser.add_argument(
        "--ext", "-e", help="text file type to search", type=str,
        default=".txt")

    return parser


def main():
    start_time = dt.now()
    parser = create_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)

    logger.addHandler(ch)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("""
    --------------------------------\n
    Starting up, time = {}\n
    --------------------------------\n
    """.format(start_time))

    logger.info(
        "Searching={} for text={} in files with ext={} every sec={}".format(
            args.direct, args.mstring, args.ext, args.interval))

    while not exit_flag:
        # logger.info(exit_flag)
        try:
            directory_recorder(args.direct, args.ext, args.mstring)

            # call my directory watching function..

        except OSError as e:
            logger.error("ERROR: {}".format(e))
            time.sleep(args.interval+2.0)
        except Exception as e:

            logger.exception("UNHANDELED EXECTPION: {}".format(e))
            time.sleep(args.interval+3.0)

        time.sleep(args.interval)

    stop_time = dt.now() - start_time
    logger.info("""
    --------------------------------\n
    Shutting down. Uptime = {}\n
    --------------------------------\n
    """.format(stop_time))
    logging.shutdown()


if __name__ == '__main__':
    main()
