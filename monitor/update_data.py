
def add_reading_to_data(reading,data):
  array = reading.split(",")
  channel = array[0]
  measure = array[1]
  timestp = array[2]
  if channel not in data:
    data[channel] = {}
  if timestp in data[channel]:
    return
  data[channel][timestp] = measure

def get_file_payload(data):
  tuples = []
  for channel in data:
    for timestp in data[channel]:
      tuples.append((channel,timestp,data[channel][timestp]))
  tuples.sort(key=lambda tup: tup[1])
  payload = []
  for channel, timestp, measure in tuples:
    payload.append(str(channel)+","+str(measure)+","+str(timestp)+";")
  return "".join(payload)

# {<channel>: {<time stamp>: <value>}}
data = {}

with open('data.csv','r') as f:
  current_data = f.read()

readings = current_data.split(";")
readings.pop()

for reading in readings:
  add_reading_to_data(reading,data)

with open('temp_data.csv','r') as f:
  new_data = f.read()

readings = new_data.split(";")
readings.pop()

for reading in readings:
  add_reading_to_data(reading,data)

data = get_file_payload(data)

with open('data.csv','w') as f:
  f.write(data)

