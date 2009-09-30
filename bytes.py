#! /usr/bin/env python

import struct

def u1(num):
    return struct.pack('B', 0x000000ff & num)

def u2(num):
    return struct.pack('BB', (0x0000ff00 & num) >> 8,
                              0x000000ff & num)

def u4(num):

    return struct.pack('BBBB', (0xff000000 & num) >> 24,
                               (0x00ff0000 & num) >> 16,
                               (0x0000ff00 & num) >> 8,
                               0x000000ff & num)

