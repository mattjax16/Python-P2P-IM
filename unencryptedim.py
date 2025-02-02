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


def p2p_message_handler(client_sock):
    while True:
        inputs, _, _ = select.select([stdin, client_sock], [], [])
        for input in inputs:
            if input == client_sock:
                try:
                    msg = client_sock.recv(20480).decode("utf-8")
                    if not msg:
                        return
                    print(msg, end="")
                except BaseException:
                    return
            else:
                try:
                    msg = stdin.readline()
                    if not msg:
                        return
                    client_sock.sendall(msg.encode("utf-8"))
                except BaseException:
                    return


def server():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("0.0.0.0", 9999))
    server_sock.listen(1)
    client_sock, addr = server_sock.accept()
    p2p_message_handler(client_sock)


def client(hostname):
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((hostname, 9999))
    p2p_message_handler(client_sock)


def shutdown(signum, frame):
    sys.stdout.flush()
    sys.exit(0)
    return


def main():
    args = get_args()
    sys.stdout.flush()

    if args.c:
        client(args.c)
    elif args.s:
        server()

    sys.stdout.flush()


if __name__ == "__main__":
    main()
