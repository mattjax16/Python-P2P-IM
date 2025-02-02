"""
unencryptedim.py

Author: Matt Bass
"""

import argparse
import socket
import sys
import select
import signal
from sys import stdin


def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--s", action="store_true")
    group.add_argument("--c", metavar="hostname", type=str)
    args = parser.parse_args()
    return args




def server():
    signal.signal(signal.SIGINT, shutdown)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("0.0.0.0", 9999))
    server_sock.listen(1)

    while True:
        inputs, _ , _ = select.select([stdin, server_sock], [], [])
        for input in inputs:
            if input == server_sock:
                try:
                    msg = server_sock.recv(2048).decode("utf-8")
                    if msg:
                        print(msg)
                except:
                    pass
            else:
                try:
                    msg = stdin.readline()
                    server_sock.sendall(msg.encode("utf-8"))
                except:
                    pass


def client(hostname):
    signal.signal(signal.SIGINT, shutdown)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((hostname, 9999))

    try:
        while True:
            msg = input()
            client_sock.sendall(msg.encode("utf-8"))

    except:
        pass



def shutdown(signum, frame):
    sys.exit(0)
    return


def main():
    args = get_args()

    if args.c:
        client(args.c)
    elif args.s:
        server()

    print("done")


if __name__ == "__main__":
    main()
