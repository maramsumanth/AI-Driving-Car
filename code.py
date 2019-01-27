import RPi.GPIO as GPIO
import time
from time import sleep
import csv

in1 = 24 #pin 16
in2 = 23 #pin 18
en = 25 #pin 22
temp1=1


TRIG = 27 #pin 13
ECHO = 22 #pin 15

print("Distance Measurement In Progress")

GPIO.setmode(GPIO.BCM) 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)



p=GPIO.PWM(en,1000)
p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

while(1):

    x=raw_input()
    
    if x=='r':
        print("run")
        if(temp1==1):
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            print("forward")
            x='z'
            time.sleep(5)
            GPIO.output(TRIG, False)
            print("Waiting For Sensor To Settle")
            time.sleep(2)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            while GPIO.input(ECHO)==0:
                pulse_start = time.time()
            while GPIO.input(ECHO)==1:
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
 
            distance = pulse_duration * 17150
 
            distance = round(distance, 2)
 
            print("Distance:",distance,"cm")
            GPIO.cleanup()


         
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            print("backward")
            x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")








 

 

 


 

 

 

