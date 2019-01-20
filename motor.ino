void setup() {
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(5,OUTPUT);
}

void loop() {
  
   digitalWrite(8,HIGH);
   digitalWrite(7,LOW);
   analogWrite(9,200);
   
   digitalWrite(5,HIGH);
   digitalWrite(6,LOW);
   analogWrite(10,200);
   delay(2000);

   digitalWrite(5,HIGH);
   digitalWrite(6,LOW);
   analogWrite(10,0);
   delay(1000);
}
