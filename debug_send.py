#!/usr/bin/python

import sys
import socket

def main():
    if len(sys.argv) <= 2:
        print "Usage: {0} socket message".format(sys.argv[0])
        sys.exit(1)

    socket_path = sys.argv[1]
    message = ' '.join(sys.argv[2:])

    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    s.sendto(message, socket_path)

if __name__ == "__main__":
    main()
