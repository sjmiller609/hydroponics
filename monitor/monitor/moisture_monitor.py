#!/usr/env/bin python

from adc import adc
from time import time, sleep
from threading import Lock
from thread import start_new_thread
from threading import Thread
import json

class HydrationMonitor():

    def __init__(self,channels,log='hydration.csv',write_period=30):
        self.kill_switch = False
        self.write_period = write_period
        self.timer = Timer()
        self.log = log
        if not channels or len(channels) == 0:
          channels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        for channel in channels:
            self.add_channel(channel)
        #self.thread = start_new_thread(self._monitor,())
        self.thread = Thread(target=self._monitor,args=())
        self.thread.start()

    def add_channel(self,channel,period=60):
        self.timer.insert(channel,period)

    def remove_channel(self,channel):
        self.timer.delete(channel)

    def stop(self):
        #raise Exception("not working yet.")
        self.kill_switch = True
        self.thread.join()

    def _monitor(self):
        while(not self.kill_switch):
            sleep(self.write_period)
            readings = self.timer.get_readings()
            if len(readings) > 0:
                writeme = []
                for channel, reading, _time in readings:
                    writeme += [str(channel),",",str(reading),",",str(_time),";"]
                writeme = "".join(writeme)
                print("writing "+str(len(readings))+" to "+self.log)
                with open(self.log,"a") as f:
                    f.write(writeme)
        self.timer.kill()

class Node():
    def __init__(self,channel,period,remaining):
        if channel is not None:
            self.channel = adc.Channel(channel)
        self.num = channel
        self.period = period
        self.remaining = remaining
        self._next = None
        print("new node created: "+str(channel)+","+str(period)+","+str(remaining))

    def __str__(self):
        build_json = {}
        build_json["channel"] = self.num
        build_json["remaining"] = self.remaining
        build_json["period"] = self.period
        return json.dumps(build_json)

class Timer():
    def __init__(self,sample_period = 1, refresh_channels_period=60*10):
        #dummy node
        self.sample_period = sample_period
        self.front = Node(None,None,None)
        self.last_reading = time()
        self.lock = Lock()
        self.readings = []
        self.channels = set()
        self.kill_switch = False
        #self.thread = start_new_thread(self._thread,())
        self.thread = Thread(target=self._thread,args=())
        self.thread.start()

    def get_readings(self):
        with self.lock:
            result = list(self.readings)
            self.readings = []
            return result

    def _thread(self):
        while(not self.kill_switch):
            sleep(self.sample_period)
            self.sample()

    def _dequeue(self):
        time_since_last_reading = time() - self.last_reading
        if time_since_last_reading < 1:
            print("reading too quickly: sleeping "+str(time_since_last_reading)+"s")
            sleep(1 - time_since_last_reading)
        reading = self.front._next.channel.getreading()
        _time = time()
        self.last_reading = _time
        num = self.front._next.num
        period = self.front._next.period
        self.channels.remove(num)
        print("dequeuing: "+str(self.front._next))
        self.front._next = self.front._next._next
        print("got reading: ")
        build_json = {}
        build_json["reading"] = reading
        build_json["channelnum"] = num
        build_json["period"] = period
        build_json["time"] = _time
        print(json.dumps(build_json))
        print("")
        return reading, num, period, _time

    def sample(self):
        with self.lock:
            #print("front node:")
            #print(str(self.front._next))
            #print("sampling...")
            subtract = self.sample_period
            while self.front._next:
                if self.front._next.remaining > subtract:
                    self.front._next.remaining -= subtract
                    return
                else:
                    subtract -= self.front._next.remaining
                    reading, channel, period, _time = self._dequeue()
                    self.readings.append((channel,reading,_time))
                    if reading > 0.00: #if we got a reading, continue to read
                        self._insert(channel,period)
                    else:
                        print("channel "+str(channel)+" got a reading "+str(reading)+", stopping recording on this channel.")
            #print("front node after sample:")
            #print(str(self.front._next))
            #print()

    def insert(self,channel,period):
        with self.lock:
            self._insert(channel,period)
                
    def _insert(self,channel,period):
        if channel in self.channels:
            #raise AttributeError("channel already inserted.")
            return #don't throw error, just do nothing
        self.channels.add(channel)
        wait = period
        prev = self.front
        _next = prev._next
        while _next and wait > _next.remaining:
            wait -= _next.remaining
            prev = _next
            _next = prev._next
        new_node = Node(channel,period,wait)
        new_node._next = prev._next
        prev._next = new_node
        if new_node._next is not None:
            new_node._next.remaining -= wait

    def delete(self,channel):
        #TODO
        raise Exception("not implemented: delete")

    def kill(self):
        self.kill_switch = True
        self.thread.join()

if __name__ == "__main__":
    monitor = None
    while True:
        #every 10 minutes, refresh checking all the channels
        print("refreshing channels...")
        monitor = HydrationMonitor([])
        sleep(60*10)
        monitor.stop()
        sleep(15)
