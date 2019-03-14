import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
import csv
import numpy as np
import pandas as pd
 
A = pd.read_csv("/home/pi/Desktop/training_data/sens5.csv")
B = pd.read_csv("/home/pi/Desktop/training_data/sens6.csv")
C = pd.read_csv("/home/pi/Desktop/training_data/sens7.csv")
X = np.hstack([A,B,C])
y = pd.read_csv("/home/pi/Desktop/training_data/ctrlnum2.csv")
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform( X )
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=10, oob_score=True, random_state=123456, max_depth=10,n_jobs=-1)
rf.fit(X,y)
print("Done Training")
#set GPIO Pins
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
#p1.start(44)
 
p2 = GPIO.PWM(enB,1000)
#p2.start(44)
 
def distance():
    #print(1)
    # set Trigger to HIGH
    GPIO.output(TRIG1, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIG1, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(ECHO1) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(ECHO1) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = int((TimeElapsed * 34300) / 2)
    #print(distance)
    return distance
def distance2():
    # set Trigger to HIGH
    GPIO.output(TRIG2, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIG2, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(ECHO2) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(ECHO2) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
   
    distance2 = int((TimeElapsed * 34300) / 2)
    #print(distance2)
    return distance2
def distance3():
    # set Trigger to HIGH
    GPIO.output(TRIG3, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIG3, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(ECHO3) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(ECHO3) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance3 = int((TimeElapsed * 34300) / 2)
    #print(distance3)
    return distance3
 
         
if __name__ == '__main__':
    try:
        while True:
            sensor1 = distance()
            sensor2 = distance2()
            sensor3 = distance3()
            if (sensor3 <= 2):
                p1.start(50)
 
		#p2 = GPIO.PWM(enB,1000)
		p2.start(50)

                #print(sensor3,sensor2,sensor1) 
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                print("backward")

            if (sensor1 <= 4):
                p1.start(35)

		p2.start(45)
                #print(sensor3,sensor2,sensor1) 
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                print("left")

            if (sensor2 <= 4):
                p1.start(45)
 
		#p2 = GPIO.PWM(enB,1000)
		p2.start(35) 
                GPIO.output(in2,GPIO.LOW)
     	        GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                print("right")


         

            yolo = np.array([sensor3,sensor2,sensor1])
            yolo.reshape(3,1)
            new = np.reshape(yolo, (1, 3))
            new = scaler.transform(new)
            ytest = rf.predict(new)
            FLAG = int(ytest[0])
            if FLAG == 1: #Forward
		#p1 = GPIO.PWM(enA,1000)
		p1.start(45)
 
		#p2 = GPIO.PWM(enB,1000)
		p2.start(45)

                print("forward")
                #print(sensor3,sensor2,sensor1) 
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
       	        GPIO.output(in3,GPIO.LOW)
            
   
            elif FLAG == 2: #Right
		#time.sleep(0.4)
		print("right")
                #print(sensor3,sensor2,sensor1)
		#p1 = GPIO.PWM(enA,1000)
		p1.start(45)
 
		#p2 = GPIO.PWM(enB,1000)
		p2.start(35) 
                GPIO.output(in2,GPIO.LOW)
     	        GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
            

            elif FLAG == 3: #Left
		#time.sleep(0.4)
		#p1 = GPIO.PWM(enA,1000)
		p1.start(35)

		p2.start(45)

	        print("left")
                #print(sensor3,sensor2,sensor1) 
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                

            elif FLAG == 4: #Backward
		print("backward")
		#p1 = GPIO.PWM(enA,1000)
		p1.start(50)
 
		#p2 = GPIO.PWM(enB,1000)
		p2.start(50)

                #print(sensor3,sensor2,sensor1) 
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                
 
            print(yolo)
 
    except:
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
        pass
