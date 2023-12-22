#!/usr/bin/env python
# -*- coding: utf-8 -*-
import select
import socket
import struct
import time
from math import *

# List of socket objects that are currently open
open_sockets = []

# AF_INET means IPv4.
# SOCK_STREAM means a TCP connection.
# SOCK_DGRAM would mean an UDP "connection".
listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# The parameter is (host, port).
# The host, when empty or when 0.0.0.0, means to accept connections for
# all IP addresses of current machine. Otherwise, the socket will bind
# itself only to one IP.
# The port must greater than 1023 if you plan running this script as a
# normal user. Ports below 1024 require root privileges.
listening_socket.bind(("", 10001))

# The parameter defines how many new connections can wait in queue.
# Note that this is NOT the number of open connections (which has no limit).
# Read listen(2) man page for more information.
listening_socket.listen(5)

current_position = []


def print_pos(ra_int, dec_int):
    """Calculate and print the recieved right ascension and declination sent by Stellarium."

    Args:
        ra_int (int): Stellarium protocol's RA
        dec_int (int): Stellarium protocol's declination
    """
    h = ra_int
    d = floor(0.5 + dec_int * (360 * 3600 * 1000 / 4294967296.0))
    dec_sign = ""
    if d >= 0:
        if d > 90 * 3600 * 1000:
            d = 180 * 3600 * 1000 - d
            h += 0x80000000
        dec_sign = "+"
    else:
        if d < -90 * 3600 * 1000:
            d = -180 * 3600 * 1000 - d
            h += 0x80000000
        d = -d
        dec_sign = "-"

    h = floor(0.5 + h * (24 * 3600 * 10000 / 4294967296.0))
    ra_ms = h % 10000
    h /= 10000
    ra_s = h % 60
    h /= 60
    ra_m = h % 60
    h /= 60

    h %= 24
    dec_ms = d % 1000
    d /= 1000
    dec_s = d % 60
    d /= 60
    dec_m = d % 60
    d /= 60

    print(f"Right ascension (RA): {h}h {ra_m}m {ra_s}.{ra_ms}s")
    print(f"Declination (Dec): {dec_sign}{d}d {dec_m}m {dec_s}.{dec_ms}s")


while True:
    # Waits for I/O being available for reading from any socket object.
    rlist, wlist, xlist = select.select([listening_socket] + open_sockets, [], [])
    for i in rlist:
        if i is listening_socket:
            new_socket, addr = listening_socket.accept()
            open_sockets.append(new_socket)
        else:
            data = i.recv(1024)
            if data == "":
                open_sockets.remove(i)
                print("Connection closed")
            else:
                print(repr(data))
                data = struct.unpack(
                    "3iIi",  # 3 unsigned ints, a signed int, and another unsigned int
                    data,
                )
                print("%x, %o" % (data[3], data[3]))
                ra = data[3] * (pi / 0x80000000)
                dec = data[4] * (pi / 0x80000000)
                cdec = cos(dec)

                desired_pos = []
                desired_pos.append(cos(ra) * cdec)
                desired_pos.append(sin(ra) * cdec)
                desired_pos.append(sin(dec))
                print_pos(data[3], data[4])
                print(desired_pos)

                # Set desired position and get current
                # send current position back to client
                # update current position

                reply = struct.pack(
                    "3iIii",  # 3 unsigned ints, a signed int, and another two unsigned ints
                    24,
                    0,
                    int(time.time()),
                    data[3],
                    data[4],
                    0,
                )
                # print repr(reply)

                i.send(reply)
