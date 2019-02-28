import RPi.GPIO as GPIO
import time

#GPIO SETUP
print("Setting up gpio...")
GPIO.setmode(GPIO.BCM)
FLAME = 21
GPIO.setup(FLAME, GPIO.IN)
TRIG = 23
ECHO = 24
flame_detect = False
pot_detect = False
GPIO.add_event_detect(FLAME, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW

def dist_sensor():
    global pot_detect
    while pot_detect == False:
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
        print ("Distance is: ",dist,"cm")
        if dist <= 5:
            pot_detect = True
 
def callback(FLAME):
    global flame_detect
    if GPIO.input(FLAME): #if pin is HIGH
        print("Flame detected")
        flame_detect = True
    else:
        print("No flame detected")
        flame_detect = False
GPIO.add_event_callback(FLAME, callback)  # assign function to GPIO PIN, Run function on change

def check_input():
    dist_sensor()
    print ("Flame is now",flame_detect)
    print ("Pot is now",pot_detect)
    if pot_detect == True and flame_detect == True:
        print ("Flame and Pot detected!")
        cooking = True
    else:
        cooking = False
    return cooking
 
    

# infinite loop
while True:
    cooking = check_input()
    if cooking == True:
        GPIO.cleanup()
        break
    else:
        time.sleep(1)