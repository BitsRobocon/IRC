int echo1=A1,trig1=41,enable1=2,motinph1=39,motinpl1=38;
int echo2=A2,trig2=42,enable2=3,motinph2=37,motinpl2=36;
int echo3=A3,trig3=43,enable3=4,motinph3=35,motinpl3=34;
int echo4=A4,trig4=44,enable4=5,motinph4=32,motinpl4=33;

void setup()
{
  pinMode(enable1,OUTPUT);
  pinMode(enable2,OUTPUT);
  pinMode(enable3,OUTPUT);
  pinMode(enable4,OUTPUT);
  pinMode(motinph1,OUTPUT);
  pinMode(motinph2,OUTPUT);
  pinMode(motinph3,OUTPUT);
  pinMode(motinph4,OUTPUT);
  pinMode(motinpl1,OUTPUT);
  pinMode(motinpl2,OUTPUT);
  pinMode(motinpl3,OUTPUT);
  pinMode(motinpl4,OUTPUT);
  digitalWrite(motinph1,HIGH);
  digitalWrite(motinpl1,LOW);
  digitalWrite(motinph2,HIGH);
  digitalWrite(motinpl2,LOW);
  digitalWrite(motinph3,HIGH);
  digitalWrite(motinpl3,LOW);
  digitalWrite(motinph4,HIGH);
  digitalWrite(motinpl4,LOW);
  analogWrite(2,0);
  analogWrite(3,0);
  analogWrite(4,100);
  analogWrite(5,0);
}
void loop()
{
}

