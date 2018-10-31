int echo1=A1,trig1=41,enable1=5,motinph1=32,motinpl1=33;
int echo2=A2,trig2=42,enable2=2,motinph2=34,motinpl2=35;
int echo3=A3,trig3=43,enable3=3,motinph3=36,motinpl3=37;
int echo4=A4,trig4=44,enable4=4,motinph4=38,motinpl4=39;

float distance1,distance2,distance3,distance4;

int frontDistance;
int backDistance;
int rightDistance;
int leftDistance;
int rightMotorH;
int leftMotorH;
int rightMotorL;
int leftMotorL;
int enableMotorR;
int enableMotorL;

int motorSpeed=128;
int moveTime=10;

void HeadingOne()
{
    frontDistance=distance1;
    backDistance=distance3;
    rightDistance=distance4;
    leftDistance=distance2;
    rightMotorH=motinph4;
    leftMotorH=motinph2;
    rightMotorL=motinpl4;
    leftMotorL=motinpl2;
    enableMotorR=enable4;
    enableMotorL=enable2;
}

void HeadingTwo()
{
    frontDistance=distance2;
    backDistance=distance4;
    rightDistance=distance1;
    leftDistance=distance3;
    rightMotorH=motinph1;
    leftMotorH=motinph3;
    rightMotorL=motinpl1;
    leftMotorL=motinpl3;
    enableMotorR=enable1;
    enableMotorL=enable3;
}

void HeadingThree()
{
    frontDistance=distance3;
    backDistance=distance1;
    rightDistance=distance2;
    leftDistance=distance4;
    rightMotorH=motinph2;
    leftMotorH=motinph4;
    rightMotorL=motinpl2;
    leftMotorL=motinpl4;
    enableMotorR=enable2;
    enableMotorL=enable4;
}

void HeadingFour()
{
    frontDistance=distance4;
    backDistance=distance2;
    rightDistance=distance1;
    leftDistance=distance3;
    rightMotorH=motinph1;
    leftMotorH=motinph3;
    rightMotorL=motinpl1;
    leftMotorL=motinpl3;
    enableMotorR=enable1;
    enableMotorL=enable3;
}

void MoveForward()
{

    digitalWrite(rightMotorH,HIGH);
    digitalWrite(rightMotorL,LOW);
    digitalWrite(leftMotorH,HIGH);
    digitalWrite(leftMotorL,LOW);
    analogWrite(enableMotorR,motorSpeed);
    analogWrite(enableMotorL,motorSpeed);
    delayMicroseconds(moveTime);
}

void Stop()
{
    analogWrite(enableMotorR,0);
    analogWrite(enableMotorL,0);
    digitalWrite(rightMotorH,LOW);
    digitalWrite(rightMotorL,LOW);
    digitalWrite(leftMotorH,LOW);
    digitalWrite(leftMotorL,LOW);
}

void Ultrasound()
{
  digitalWrite(trig1,LOW);
  delayMicroseconds(2);
  
  digitalWrite(trig1,HIGH);
  delayMicroseconds(10);

  digitalWrite(trig1,LOW);
  distance1=.017*pulseIn(echo1,HIGH);
  
  digitalWrite(trig2,LOW);
  delayMicroseconds(2);
  
  digitalWrite(trig2,HIGH);  
  delayMicroseconds(10);

  digitalWrite(trig2,LOW);  
  distance2=.017*pulseIn(echo2,HIGH);
  
  digitalWrite(trig3,LOW);
  delayMicroseconds(2);
  
  digitalWrite(trig3,HIGH);  
  delayMicroseconds(10);

  digitalWrite(trig3,LOW);
  distance3=.017*pulseIn(echo3,HIGH);
  
  digitalWrite(trig4,LOW);
  delayMicroseconds(2);
  
  digitalWrite(trig4,HIGH);  
  delayMicroseconds(10);

  digitalWrite(trig4,LOW);
  distance4=.017*pulseIn(echo4,HIGH);
}
void setup() {
pinMode(echo1,INPUT);pinMode(trig1,OUTPUT);pinMode(enable1,OUTPUT);pinMode(motinph1,OUTPUT);pinMode(motinpl1,OUTPUT);
pinMode(echo2,INPUT);pinMode(trig2,OUTPUT);pinMode(enable2,OUTPUT);pinMode(motinph2,OUTPUT);pinMode(motinpl2,OUTPUT);
pinMode(echo3,INPUT);pinMode(trig3,OUTPUT);pinMode(enable3,OUTPUT);pinMode(motinph3,OUTPUT);pinMode(motinpl3,OUTPUT);
pinMode(echo4,INPUT);pinMode(trig4,OUTPUT);pinMode(enable4,OUTPUT);pinMode(motinph4,OUTPUT);pinMode(motinpl4,OUTPUT);

digitalWrite(trig1,LOW);
digitalWrite(trig2,LOW);
digitalWrite(trig3,LOW);
digitalWrite(trig4,LOW);

Ultrasound();

HeadingOne();
Serial.begin(9600);
}

void loop() {
  Ultrasound();
  HeadingFour();
  MoveForward();
  Serial.print("distance1 : ");
  Serial.println(distance1);
  Serial.print("distance2 : ");
  Serial.println(distance2);
  Serial.print("distance3 : ");
  Serial.println(distance3);
  Serial.print("distance4 : ");
  Serial.println(distance4);
  Serial.println();  
}
