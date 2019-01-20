int motorLpin1=2;
int motorLpin2=3;
int motorRpin1=4;
int motorRpin2=5;
int motorLpwm=10;
int motorRpwm=11;

int motorSpeed=125;
int turn=50;

void setup() {
  Serial.begin(9600);
  Serial.flush();
  pinMode(motorLpin1,OUTPUT);
  pinMode(motorLpin2,OUTPUT);
  pinMode(motorRpin1,OUTPUT);
  pinMode(motorRpin2,OUTPUT);
  pinMode(motorLpwm,OUTPUT);
  pinMode(motorRpwm,OUTPUT);
}

void loop() {
  String input="";
  while(Serial.available()){
    input+=(char)Serial.read();
    delay(5);
  }
  
  if(input=="n"){
    stp();
  }
  else if(input=="F"){
    fwd();
  }
  else if(input=="R"){
    rev();
  }
  else if(input.indexOf("TL")>-1){
    lft();
  }
  else if(input.indexOf("TR")>-1){
    rght();
  }
  else if(input!=""){
    motorSpeed=input.toInt();
  }
}

void fwd(){
  analogWrite(motorLpwm,motorSpeed);
  analogWrite(motorRpwm,motorSpeed);
  digitalWrite(motorLpin1,1);
  digitalWrite(motorLpin2,0);
  digitalWrite(motorRpin1,1);
  digitalWrite(motorRpin2,0);
}

void rev(){
  analogWrite(motorLpwm,motorSpeed);
  analogWrite(motorRpwm,motorSpeed);
  digitalWrite(motorLpin1,0);
  digitalWrite(motorLpin2,1);
  digitalWrite(motorRpin1,0);
  digitalWrite(motorRpin2,1);
}

void lft(){
  analogWrite(motorLpwm,motorSpeed-turn);
  analogWrite(motorRpwm,motorSpeed+turn);
  digitalWrite(motorLpin1,0);
  digitalWrite(motorLpin2,1);
  digitalWrite(motorRpin1,1);
  digitalWrite(motorRpin2,0);
}

void rght(){
  analogWrite(motorLpwm,motorSpeed+turn);
  analogWrite(motorRpwm,motorSpeed-turn);
  digitalWrite(motorLpin1,1);
  digitalWrite(motorLpin2,0);
  digitalWrite(motorRpin1,0);
  digitalWrite(motorRpin2,1);
}

void stp(){
  analogWrite(motorLpwm,0);
  analogWrite(motorRpwm,0);
  digitalWrite(motorLpin1,1);
  digitalWrite(motorLpin2,1);
  digitalWrite(motorRpin1,1);
  digitalWrite(motorRpin2,1);
}
