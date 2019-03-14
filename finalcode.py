import RPi.GPIO as GPIO
import time
import csv
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


GPIO.setwarnings(False)
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

A = pd.read_csv("sensor1.csv")
B = pd.read_csv("sensor2.csv")
C = pd.read_csv("sensor3.csv")
X = np.hstack([A,B,C])
y = pd.read_csv("commands.csv")

scaler = StandardScaler()
X = scaler.fit_transform(X)
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators = 10, oob_score = True, random_state = 123456, max_depth = 10, n_jobs = -1)
rf.fit(X,y)
print("Done Training")

#Motor Driver
in1 = 16 #pin 36
in2 = 19 #pin 35
in3 = 23 #pin 16
in4 = 24 #pin 18
enA = 20 #pin 38
enB = 25 #pin 22

#ULtrasonic Sensors
TRIG1 = 27 #pin 13
ECHO1 = 22 #pin 15
TRIG2 = 5 #pin29
ECHO2 = 6 #pin31
TRIG3 = 17 #pin11
ECHO3 = 26 #pin37
 
#set GPIO direction (IN / OUT)
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
p2 = GPIO.PWM(enB,1000)


def distance1():

    GPIO.output(TRIG1, True)
    time.sleep(0.00001)
    GPIO.output(TRIG1, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(ECHO1) == 0:
        StartTime = time.time()

    while GPIO.input(ECHO1) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance1 = int((TimeElapsed * 34300) / 2)
    return distance1


def distance2():

    GPIO.output(TRIG2, True)
    time.sleep(0.00001)
    GPIO.output(TRIG2, False)
 
    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(ECHO2) == 0:
        StartTime = time.time()

    while GPIO.input(ECHO2) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance2 = int((TimeElapsed * 34300) / 2)
    return distance2


def distance3():

    GPIO.output(TRIG3, True)
    time.sleep(0.00001)
    GPIO.output(TRIG3, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(ECHO3) == 0:
        StartTime = time.time()

    while GPIO.input(ECHO3) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance3 = int((TimeElapsed * 34300) / 2)
    return distance3

       
if __name__ == '__main__':
    try:
        while True:
            sensor1 = distance1()
            sensor2 = distance2()
            sensor3 = distance3()
            if (sensor3 <= 2):
                p1.start(50)
		p2.start(50)

                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                print("backward")

            if (sensor1 <= 4):
                p1.start(35)
		p2.start(45)
                 
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                print("left")

            if (sensor2 <= 4):
                p1.start(45)
		p2.start(35)

                GPIO.output(in2,GPIO.LOW)
     	        GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                print("right")
		
	    print([sensor3,sensor2,sensor1])

            yolo = np.array([sensor3,sensor2,sensor1])
            yolo.reshape(3,1)
            new = np.reshape(yolo, (1, 3))
            new = scaler.transform(new)
            ytest = rf.predict(new)
            FLAG = int(ytest[0])

            if FLAG == 1: #Forward
		p1.start(45)
		p2.start(45)

                print("forward")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
       	        GPIO.output(in3,GPIO.LOW)
            
   
            elif FLAG == 2: #Right
		p1.start(45)
		p2.start(35)

		print("right")
                GPIO.output(in2,GPIO.LOW)
     	        GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
            

            elif FLAG == 3: #Left
		p1.start(35)
		p2.start(45)

	        print("left")
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                

            elif FLAG == 4: #Backward
		p1.start(50)
		p2.start(50)
		
		print("backward")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)

            print(yolo)
 

    except:
	GPIO.output(in1, GPIO.LOW)
	GPIO.output(in2, GPIO.LOW)
	GPIO.output(in3, GPIO.LOW)
	GPIO.output(in4, GPIO.LOW)
	GPIO.output(enB, GPIO.LOW) 
	GPIO.output(enA, GPIO.LOW)

	GPIO.setup(TRIG1,GPIO.LOW)
	GPIO.setup(TRIG2,GPIO.LOW)
	GPIO.setup(TRIG3,GPIO.LOW)

	GPIO.setup(ECHO1,GPIO.LOW)
	GPIO.setup(ECHO2,GPIO.LOW)
	GPIO.setup(ECHO3,GPIO.LOW)
        pass
