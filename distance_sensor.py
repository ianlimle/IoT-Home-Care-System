import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
dist = 5

while dist >= 5:
    print ("Distance Measurement In Progress")
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    print ("Wait For Sensor To Settle")
    time.sleep(2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)

    while GPIO.input(ECHO)==0:
        start=time.time()
    while GPIO.input(ECHO)==1:
        end=time.time()
    duration= end-start
    dist = round(duration*17150,2)
    print ("Distance: ",dist,"cm")
GPIO.cleanup()