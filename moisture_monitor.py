#!/usr/env/bin python

from adc import adc
from history import logger
from time import time, sleep

class Node():
    def __init__(self,channel,period,remaining):
        self.channel = channel
        self.period = period
        self.remaining = remaining
    
class Timer():
    def __init__(self):
        self.list = LinkedList()
        self.last_time = time()
        self.lock = Lock()
        self.readings = []
        self.thread

    def get_readings(self):
        with self.lock:
            result = list(self.readings)
            self.readings = []
            return result

    def insert(self,channel,period):
        with self.lock:
            if period < self.list.front.remaining

    def delete(self,channel):

    def timer(self):


class HydrationMonitor():

    def __init__(self,channels,log='hydration.log',write_period=30):
        self.kill_switch = False
        self.write_period = write_period
        self.timer = Timer()
        for channel in channels:
            self.add_channel(channel)

    def add_channel(self,channel,period=30):
        self.timer.insert(channel,period)

    def remove_channel(self,channel):
        self.timer.delete(channel)

    def stop(self):
        self.kill_switch = True

    def monitor(self):
        while(not self.kill_switch):
            sleep(self.write_period)
            readings = self.timer.get_readings()
            for reading in readings:
                self.log(reading)
        self.timer.kill()
