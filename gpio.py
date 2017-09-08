import RPi.GPIO as GPIO

channel = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel,GPIO.IN)
result = GPIO.input(channel)
print(result)
