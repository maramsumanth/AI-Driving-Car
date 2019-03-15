#include <PS3BT.h>
#include <usbhub.h>
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

USB Usb;
BTD Btd(&Usb);  
PS3BT PS3(&Btd);

int motorSpeedA = 0;
int motorSpeedB = 0;


int rx, ry;

//Define Motor pins
#define enA 10
#define in1 22
#define in2 23
#define enB 11
#define in3 24
#define in4 25

//Define Ultrasonic Sensor pins
#define trigPin1 8   
#define echoPin1 9
#define trigPin2 4
#define echoPin2 5
#define trigPin3 6
#define echoPin3 7
 
long duration, distance, RightSensor,BackSensor,FrontSensor,LeftSensor;
 
void setup()
{
 
  Serial.begin(115200);
  #if !defined(__MIPSEL__)
  while (!Serial);
  #endif

  if (Usb.Init() == -1)
  { 
   Serial.print(F("\r\nOSC did not start"));
   while (1); //halt
  }

  Serial.print(F("\r\nPS3 Bluetooth Library Started"));

  pinMode(enA, OUTPUT);   
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);   
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);   
  pinMode(in4, OUTPUT);

  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin3, INPUT);

}
 
void loop() 
{

  Usb.Task();

  if (PS3.PS3Connected || PS3.PS3NavigationConnected)
  { 
    rx = PS3.getAnalogHat(RightHatX);
    ry = PS3.getAnalogHat(RightHatY);
    
    
    if (ry <= 115 && rx == 127)     //Forward
    { 
      Serial.println("Forward");

      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);

      motorSpeedA = map(ry, 115, 0, 0, 100);
      motorSpeedB = map(ry, 115, 0, 0, 100);
    }

    else if (ry >= 140 && rx == 127)    //Backward
    { 
      Serial.println("Backward");
     
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
      
      motorSpeedA = map(ry, 140, 255, 0, 100);
      motorSpeedB = map(ry, 140, 255, 0, 100);
      
    }

    else if (rx >= 140 && ry == 127)     //Right
    { 
      Serial.println("Right");

      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, LOW);
      digitalWrite(in4, LOW);

      motorSpeedA = map(rx, 140, 255, 0, 100);
      motorSpeedB = map(rx, 140, 255, 0, 100);
    }

    else if (rx < 115 && ry == 127)     //Left
    { 
      Serial.println("Left");

      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);
      
      motorSpeedA = map(rx, 115, 0, 0, 100);
      motorSpeedB = map(rx, 115, 0, 0, 100);
      }

    else
    { 
      Serial.println("Stop");
      motorSpeedA = 0;
      motorSpeedB = 0;
    }
   
    analogWrite(enA, motorSpeedA); // Send PWM signal to motor A
    analogWrite(enB, motorSpeedB); // Send PWM signal to motor B
    measuredist();
  }
  
}
 
void SonarSensor(int trigPin,int echoPin)
{
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distance = (duration/2) / 29.1;
 
}

void measuredist()
{
  SonarSensor(trigPin1, echoPin1);
  RightSensor = distance;
  SonarSensor(trigPin2, echoPin2);
  LeftSensor = distance;
  SonarSensor(trigPin3, echoPin3);
  FrontSensor = distance;
 
  Serial.println(FrontSensor);
  Serial.println(RightSensor);
  Serial.println(LeftSensor);      

}
