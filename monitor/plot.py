import matplotlib.dates as mdate
import matplotlib.pyplot as plt
import time
import os

with open("data.csv","r") as f:
   data = f.read()

data = data[:-1]
moistures = [float(reading.split(",")[1]) for reading in data.split(";")]
times = [float(reading.split(",")[2]) for reading in data.split(";")]
times = mdate.epoch2num(times)
fig, ax = plt.subplots()
ax.plot_date(times, moistures)

# Choose your xtick format string
date_fmt = '%d-%m-%y %H:%M:%S'

# Use a DateFormatter to set the data to the correct format.
date_formatter = mdate.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()

plt.show()
