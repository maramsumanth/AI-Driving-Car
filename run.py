import RPi.GPIO as GPIO
import time

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Training
def Model(sensor1, sensor2, sensor3):
    
    #return direction as an integer from 1 to 4
    #return 5 at the end of path (stop)
    #1 - Forward
    #2 - Left
    #3 - Right
    #4 - Backward
    #5 - Stop
    return #level



in1 = 16 #pin 36
in2 = 19 #pin 35
enA = 20 #pin 38

in3 = 23 #pin 16
in4 = 24 #pin 18
enB = 25 #pin 22

TRIG1 = 27 #pin 13
ECHO1 = 22 #pin 15

TRIG2 = 5 #pin29
ECHO2 = 6 #pin31

TRIG3 = 17 #pin11
ECHO3 = 26 #pin37



GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(TRIG3,GPIO.OUT)
GPIO.setup(ECHO3,GPIO.IN)


GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)


GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)


p1 = GPIO.PWM(enA,1000)
p1.start(25)

p2 = GPIO.PWM(enB,1000)
p2.start(25)

GPIO.output(TRIG1, False)
GPIO.output(TRIG2, False)
GPIO.output(TRIG3, False)

#Sensors to settle
time.sleep(1)

GPIO.output(TRIG1, True)
time.sleep(0.00001)
GPIO.output(TRIG1, False)

GPIO.output(TRIG2, True)
time.sleep(0.00001)
GPIO.output(TRIG2, False)

GPIO.output(TRIG3, True)
time.sleep(0.00001)
GPIO.output(TRIG3, False)


while True:
    
    sensor1 = 0
    sensor2 = 0
    sensor3 = 0
    
    while GPIO.input(ECHO1) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO1) == 1:
        pulse_end = time.time()   
    sensor1 = round((pulse_end - pulse_start)*17150, 2)
    
    while GPIO.input(ECHO2) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO2) == 1:
        pulse_end = time.time()   
    sensor2 = round((pulse_end - pulse_start)*17150, 2)
    
    while GPIO.input(ECHO3) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO3) == 1:
        pulse_end = time.time()   
    sensor3 = round((pulse_end - pulse_start)*17150, 2)
    
    FLAG = Model(sensor1, sensor2, sensor3)
    
    if FLAG == 1: #Forward
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
  
    elif FLAG == 2: #Left
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)

    elif FLAG == 3: #Right
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

    elif FLAG == 4: #Backward
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
     
    elif FLAG == 5: #Stop
        GPIO.cleanup()
        break
    
    time.sleep(0.01)
    
# Reset all the GPIO pins by setting them to LOW
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(enA, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
GPIO.output(enB, GPIO.LOW) 

GPIO.setup(TRIG1,GPIO.LOW)
GPIO.setup(TRIG2,GPIO.LOW)
GPIO.setup(TRIG3,GPIO.LOW)

GPIO.setup(ECHO1,GPIO.LOW)
GPIO.setup(ECHO2,GPIO.LOW)
GPIO.setup(ECHO3,GPIO.LOW)
