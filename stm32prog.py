__author__ = 'lex'

#import sys, os.path

import time
import struct
from serial import Serial, EIGHTBITS, PARITY_EVEN

def ser_read(sz = 1, timeout = 0.1):
    st = time.clock()
    while ser.inWaiting() < sz:
        if (time.clock() - st) > timeout:
            break;

    z = ser.inWaiting();
    if z > 0:
        if z > sz:
            z = sz
        s = ser.read(z)
    else:
        s = ''

    return s

def waitAck(timeout=0.1):
    r = ser.read()
    st = time.clock()
    while len(r) == 0:
        if (time.clock() - st) > timeout:
            print "ACK timeout"
            return False
        r = ser.read(1)

    if '\x79' in r:
        return True

    return False

def cmd_GetVersion():
#    print "cmd_Get()"
    ser.write('\x00\xff')
    if not waitAck():
#        print "Cmd NACK"
        return
#    print "Cmd ACK"

    s = ser_read(1)
    if len(s) == 0:
        return

    sz = ord(s)
#    print 'Should receive - ' + hex(sz+1) + ' bytes'

    s = ser_read(sz+1)
    waitAck()
    print 'Boot version - ' + hex(ord(s[0]))
    return ord(s[0])

def cmd_GetID():
#    print "cmd_GetID"

    ser.write('\x02\xfd')
    if not waitAck():
#        print "Cmd NACK"
        return
#    print "Cmd ACK"

    s = ser_read(1)
    if len(s) == 0:
        return

    sz = ord(s)
#    print 'Should receive - ' + hex(sz+1) + ' bytes'

    s = ser_read(sz+1)
    waitAck()
    print 'PID - ' + hex(ord(s[0])) + ':' + hex(ord(s[1]))
    return (ord(s[0]), ord(s[1]))

def Connect(timeout=0.1):
    ser.flush()

    ser.write('\x7f')

    st = time.clock()
    r = ser.read(1)
    while '\x79' not in r:
        if (time.clock() - st) > timeout:
            return False
        r = ser.read()

    print 'Connect'
    return True

ser = Serial('/dev/tty.usbserial', baudrate=115200, bytesize=EIGHTBITS, parity=PARITY_EVEN, timeout=0)

Connect()
cmd_GetVersion()
cmd_GetID()
