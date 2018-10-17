void setup() {
 pinMode(9,OUTPUT);
 pinMode(10,OUTPUT);
 pinMode(8,OUTPUT);
}

void loop() 
{
  digitalWrite(8,HIGH);
  digitalWrite(10,LOW);
  analogWrite(9,180);
  delay(1000);
  digitalWrite(8,HIGH);
  digitalWrite(10,LOW);
  analogWrite(9,20);
  delay(10000);
  digitalWrite(8,LOW);
  digitalWrite(10,HIGH);
  analogWrite(9,180);
  delay(1000);
}
