"""
unencryptedim.py

Author: Matt Bass
"""

import argparse
import socket
import sys
import select
import signal


def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('--s', action="store_true")
    group.add_argument('--c', metavar='hostname', type=str)
    args = parser.parse_args()
    return args


def server():
    return


def client():
    return


def shutdown():

    return

def main():
    args = get_args()

    if args.c:
        client()
    elif args.s:
        server()








if __name__ == "__main__":
    main()
