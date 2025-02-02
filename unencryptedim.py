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
        client_sock, client_addr = server_sock.accept()
        print("Connection From", client_addr)

        try:
            while True:
                msg = client_sock.recv(2048).decode("utf-8")
                print(msg)

        except KeyboardInterrupt:
            pass
        finally:
            client_sock.close()
            server_sock.close()
            sys.exit(0)


def client(hostname):
    signal.signal(signal.SIGINT, shutdown)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((hostname, 9999))

    try:
        while True:
            msg = input()
            client_sock.sendall(msg.encode("utf-8"))

    except KeyboardInterrupt:
        pass
    finally:
        client_sock.close()
        sys.exit(0)


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
