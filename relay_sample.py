import RPi.GPIO as GPIO
from time import sleep

# Use the BCM GPIO numbers as the numbering scheme
GPIO.setmode(GPIO.BCM)

# Use GPIO17 for gas valve, other GPIO can be used as well
relay = 17

# Set GPIO23 as output.
GPIO.cleanup()
GPIO.setup(relay, GPIO.OUT)

while True:
    GPIO.output(relay, GPIO.HIGH) # turn on the gas valve
    sleep(2)
    GPIO.output(relay, GPIO.LOW) # turn off the gas valve
    sleep(1)
