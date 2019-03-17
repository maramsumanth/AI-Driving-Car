AI-Driving-Car
=============
      
## Overview

   This project is based on creating a autonomous car which is capable of sensing its environment and moving without human input. Basically it consists of 3 ultrasonic sensors attached to the front, left and right portions of car, these will calculate the obstacle distances infront of them and send them to the pretrained Machine Learning Algorithm. This will return a command, which is sent to the motors and move in the desired direction (Forward/Left/Right/Backward) accordingly.
   
## Steps to reproduce
   Clone this repo ```git clone https://github.com/maramsumanth/AI-Driving-Car.git```, change to the current directory and run finalcode.py
      

## Hardware Requirements
      Raspberry Pi          - 1
      L298N Motor Driver    - 1
      Bread Board (Small)   - 1
      LIPO Battery          - 1
      Chasis                - 1
      Power bank            - 1
      Wheels                - 2
      Motors                - 2
      Ultrasonic Sensors    - 3
      PS3 Controller for collecting data
      Jumper wires as needed
    
## Data Collection and Model Training

   Data is collected on different mazes using arduino, where the car is controlled using PS3 controller. It is stored in text file of the form ```Command, Sensor1, Sensor2, Sensor3``` each of them are seperated by lines. Make sure to filter out the data with the Stop command in the dataset before training. Using python code this dataset is converted into sensor and command files. Finally it is trained using Random Forest Classifier(Machine Learning Algorithm), with accuracy of 93%.

## Sample maze

![IMG-20190124-WA0010](https://user-images.githubusercontent.com/32808381/54482270-0be68980-4867-11e9-9c71-4d268ae18d44.jpg)




## Setup (For Linux)
Make sure that all these files are in the memory card of raspberry pi.
      If your Pi and laptop are on the same wifi network you can run code on Pi from your laptop with the command below.
            ssh username@ipaddress
            
[Here](https://drive.google.com/drive/folders/1Pr7gGW8ToveAyUVRObod15jswgyZrwg8) is the drive link to video demonstrating the assembly of the components and another video containing the final output of project.
      
