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
// this can be obtained from the dongle when running the sketch


int motorSpeedA = 0;
int motorSpeedB = 0;

int rx, ry;

#define enA 2       //Move
#define in1 28
#define in2 29
#define enB 3
#define in3 30
#define in4 31

#define Trigger2 22
#define Trigger3 23
#define Trigger4 24

#define Echo2 25
#define Echo3 26
#define Echo4 27

int fDist,lDist,bDist;

void setup() {
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

  pinMode(Trigger2,OUTPUT);
  pinMode(Trigger3,OUTPUT);
  pinMode(Trigger4,OUTPUT);
  pinMode(Echo2,INPUT);
  pinMode(Echo3,INPUT);
  pinMode(Echo4,INPUT);
  
  
  
  
}


void loop()
{ 
  
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
      motorSpeedA = map(ry, 115, 0, 0, 150);
      motorSpeedB = map(ry, 115, 0, 0, 150);
      
    }

    else if (ry >= 140 && rx == 127)     //Backward
    { //distcal();
      Serial.println("Backward");
      digitalWrite(in1, LOW);  //MOTOR A
      digitalWrite(in2, HIGH);
      
      digitalWrite(in3, LOW);  //MOTOR B
      digitalWrite(in4, HIGH);
      
      motorSpeedA = map(ry, 140, 255, 0, 150);
      motorSpeedB = map(ry, 140, 255, 0, 150);
      
    }

    // RightHatX (X-Axis of Right) is used for left and right control;
    else if (rx >= 140 && ry == 127)     //Right
    { //distcal();
      Serial.println("Right");
      digitalWrite(in1, LOW);  //MOTOR A   forward move
      digitalWrite(in2, LOW);
      
      digitalWrite(in3, HIGH);  //MOTOR B  backward move
      digitalWrite(in4, LOW);
      motorSpeedA = map(rx, 140, 255, 0, 150);
      motorSpeedB = map(rx, 140, 255, 0, 150);
    }

    else if (rx < 115 && ry == 127)     //Left
    { //distcal();
      Serial.println("Left");
      digitalWrite(in1, HIGH);  //MOTOR A    backward
      digitalWrite(in2, LOW);
      
      digitalWrite(in3, LOW);  //MOTOR B    forward
      digitalWrite(in4, LOW);
      
      motorSpeedA = map(rx, 115, 0, 0, 150);
      motorSpeedB = map(rx, 115, 0, 0, 150);
      
      }

    
    else
    { //distcal();
      Serial.println("Stop");
      motorSpeedA = 0;
      motorSpeedB = 0;
    }
   
    analogWrite(enA, motorSpeedA); // Send PWM signal to motor A
    analogWrite(enB, motorSpeedB); // Send PWM signal to motor B
    distcal();
    
  }
}



int distcal() {
  digitalWrite(Trigger2, LOW);
  delayMicroseconds(2);
  digitalWrite(Trigger2, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trigger2, LOW);
  fDist = pulseIn(Echo2, HIGH) * 0.034 / 2;
  digitalWrite(Trigger3, LOW);
  delayMicroseconds(2);
  digitalWrite(Trigger3, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trigger3, LOW);
  lDist = pulseIn(Echo3, HIGH) * 0.034 / 2;
  digitalWrite(Trigger4, LOW);
  delayMicroseconds(2);
  digitalWrite(Trigger4, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trigger4, LOW);
  bDist = pulseIn(Echo4, HIGH) * 0.034 / 2;
  
  Serial.println(fDist);
  Serial.println (bDist);
  Serial.println (lDist);
 
}
