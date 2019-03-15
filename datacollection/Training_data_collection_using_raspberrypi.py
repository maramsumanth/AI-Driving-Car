import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Set GPIO Pins

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
 
#Set GPIO direction (IN / OUT)
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
p1.start(45)
p2 = GPIO.PWM(enB,1000)
p2.start(45)
 
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
    distance = int((TimeElapsed * 34300) / 2)
    return distance


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
            FLAG = int(input())
	        if FLAG == 1: #Forward
                    t_end = time.time() + 0.5
                    while time.time() < t_end:
		        sensor1 = distance1()
     	                sensor2 = distance2()
                        sensor3 = distance3()
                        print(sensor1,sensor2,sensor3)

                        GPIO.output(in2,GPIO.HIGH)
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in3,GPIO.HIGH)
            	        GPIO.output(in4,GPIO.LOW)
                        print("forward")

                elif FLAG == 2: #Right
                    t_end = time.time() + 0.5
                    while time.time() < t_end:
		        sensor1 = distance1()
           		sensor2 = distance2()
            		sensor3 = distance3()
		        print(sensor1,sensor2,sensor3)

            		GPIO.output(in2,GPIO.LOW)
     	        	GPIO.output(in1,GPIO.HIGH)
        		GPIO.output(in3,GPIO.HIGH)
                	GPIO.output(in4,GPIO.LOW)
                	print("right")
   
                elif FLAG == 3: #Left
                    t_end = time.time() + 0.5
                    while time.time() < t_end:
		        sensor1 = distance1()
            		sensor2 = distance2()
            		sensor3 = distance3()
			print(sensor1,sensor2,sensor3)

                	GPIO.output(in2,GPIO.HIGH)
                	GPIO.output(in1,GPIO.LOW)
                	GPIO.output(in4,GPIO.HIGH)
                	GPIO.output(in3,GPIO.LOW)
                	print("left")
   
                elif FLAG == 4: #Backward
                    t_end = time.time() + 0.5
            	    while time.time() < t_end:
		        sensor1 = distance1()
            	    	sensor2 = distance2()
                    	sensor3 = distance3()
			print(sensor1,sensor2,sensor3)

                    	GPIO.output(in2,GPIO.LOW)
                    	GPIO.output(in1,GPIO.HIGH)
                    	GPIO.output(in3,GPIO.LOW)
                    	GPIO.output(in4,GPIO.HIGH)
                    	print("backward")
 
    except:
        pass
