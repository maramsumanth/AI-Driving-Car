#include <PS3BT.h>
#include <usbhub.h>
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>      //Serial Peripheral Interface and it is a way to send data between microcontrollers and other small devices

USB Usb;              //USBHub Hub1(&Usb); // Some dongles have a hub inside

BTD Btd(&Usb);        // You have to create the Bluetooth Dongle instance like so
/* You can create the instance of the class in two ways */
PS3BT PS3(&Btd);    // This will just create the instance
//PS3BT PS3(&Btd, 0x00, 0x15, 0x83, 0x3D, 0x0A, 0x57);    // This will also store the bluetooth address -
// this can be obt


int motorSpeedA = 0;
int motorSpeedB = 0;


int rx, ry;

#define enA 10       //Move
#define in1 22
#define in2 23
#define enB 11
#define in3 24
#define in4 25


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
    while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
  #endif

  if (Usb.Init() == -1)
  { Serial.print(F("\r\nOSC did not start"));
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
 
void loop() {

  Usb.Task();

  if (PS3.PS3Connected || PS3.PS3NavigationConnected)
  { //Serial.println(PS3.getAnalogHat(RightHatY));Serial.println(PS3.getAnalogHat(RightHatX));
    
    //RightHatY (Y-Axis of Right) used for forward and backward control
    rx = PS3.getAnalogHat(RightHatX);
    ry = PS3.getAnalogHat(RightHatY);
    
    
    if (ry <= 115 && rx == 127)     //Forward
    { //distcal();
      Serial.println("Forward");
      digitalWrite(in1, HIGH);  //MOTOR A    // Also HIGH for clockwise (Set accordingly)
      digitalWrite(in2, LOW);
      
      digitalWrite(in3, HIGH);  //MOTOR B
      digitalWrite(in4, LOW);
      motorSpeedA = map(ry, 115, 0, 0, 100);
      motorSpeedB = map(ry, 115, 0, 0, 100);
      
    }

    else if (ry >= 140 && rx == 127)     //Backward
    { //distcal();
      Serial.println("Backward");
      digitalWrite(in1, LOW);  //MOTOR A
      digitalWrite(in2, HIGH);
      
      digitalWrite(in3, LOW);  //MOTOR B
      digitalWrite(in4, HIGH);
      
      motorSpeedA = map(ry, 140, 255, 0, 100);
      motorSpeedB = map(ry, 140, 255, 0, 100);
      
    }

    // RightHatX (X-Axis of Right) is used for left and right control;
    else if (rx >= 140 && ry == 127)     //Right
    { //distcal();
      Serial.println("Right");
      digitalWrite(in1, HIGH);  //MOTOR A   forward move
      digitalWrite(in2, LOW);
      
      digitalWrite(in3, LOW);  //MOTOR B  backward move
      digitalWrite(in4, LOW);
      motorSpeedA = map(rx, 140, 255, 0, 100);
      motorSpeedB = map(rx, 140, 255, 0, 100);
    }

    else if (rx < 115 && ry == 127)     //Left
    { //distcal();
      Serial.println("Left");
      digitalWrite(in1, LOW);  //MOTOR A    backward
      digitalWrite(in2, LOW);
      
      digitalWrite(in3, HIGH);  //MOTOR B    forward
      digitalWrite(in4, LOW);
      
      motorSpeedA = map(rx, 115, 0, 0, 100);
      motorSpeedB = map(rx, 115, 0, 0, 100);
      
      }

    
    else
    { //distcal();
      Serial.println("Stop");
      motorSpeedA = 0;
      motorSpeedB = 0;
    }
   
    analogWrite(enA, motorSpeedA); // Send PWM signal to motor A
    analogWrite(enB, motorSpeedB); // Send PWM signal to motor B
    //distcal();
    xyz();
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

void xyz()
{
  SonarSensor(trigPin1, echoPin1);
  RightSensor = distance;
  SonarSensor(trigPin2, echoPin2);
  LeftSensor = distance;
  SonarSensor(trigPin3, echoPin3);
  FrontSensor = distance;
 
  Serial.println(LeftSensor);   //actual front @ashish
  //Serial.print(" - ");
  Serial.println(FrontSensor);    //actual right @ashish
  //Serial.print(" - ");
  Serial.println(RightSensor);      //actual left @ashish

}
