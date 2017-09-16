#!/usr/bin/python

import time
import smbus
import sys
import os, commands
import subprocess

from smbus import SMBus
from sys import exit

class Channel():
    def __init__(self,channel,vref=2.5):
        self.bus = SMBus(1)

        self.address = 0b1110110

        channels = 16*[None]
        channels[0]      =     0xB0
        channels[1]      =     0xB8
        channels[2]      =     0xB1
        channels[3]      =     0xB9
        channels[4]      =     0xB2
        channels[5]      =     0xBA
        channels[6]      =     0xB3
        channels[7]      =     0xBB
        channels[8]      =     0xB4
        channels[9]      =     0xBC
        channels[10]     =     0xB5
        channels[11]     =     0xBD
        channels[12]     =     0xB6
        channels[13]     =     0xBE
        channels[14]     =     0xB7
        channels[15]     =     0xBF
        self.channel = channels[channel]

        self.vref = vref

        # To calculate the voltage, the number read in is 3 bytes. The first bit is ignored. 
        # Max reading is 2^23 or 8,388,608
        #

        self.max_reading = 8388608.0

        self.lange = 0x06 # number of bytes to read in the block

    def getreading(self):
        self.bus.write_byte(self.address, self.channel)
        time.sleep(0.4)
        reading  = self.bus.read_i2c_block_data(self.address, self.channel, self.lange)
        valor = ((((reading[0]&0x3F))<<16))+((reading[1]<<8))+(((reading[2]&0xE0)))
        volts = valor*self.vref/self.max_reading
        return volts
