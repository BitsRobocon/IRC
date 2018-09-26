byte en1=11,en2=10,en3=9,en4=12; 
byte mi1=33,mi2=30,mi3=29,mi4=34;
byte mo1=32,mo2=31,mo3=28,mo4=35;
byte t1=32,e1=33,t2=34,e2=35,t3=36,e3=37,t4=38,e4=39;
byte mi5=40,mi6=42,mi7=44,mi8=46;
byte mo5=41,mo6=43,mo7=45,mo8=47;
int d,du;
int a,b;
void setup() {
  // put your setup code here, to run once:
pinMode(en1,OUTPUT);//mo = front, mi = back
pinMode(en2,OUTPUT);
pinMode(en3,OUTPUT);
pinMode(en4,OUTPUT);
pinMode(mo1,OUTPUT);
pinMode(mo2,OUTPUT);
pinMode(mo3,OUTPUT);
pinMode(mo4,OUTPUT);
pinMode(mi1,OUTPUT);
pinMode(mi2,OUTPUT);
pinMode(mi3,OUTPUT);
pinMode(mi4,OUTPUT);
pinMode(mo5,OUTPUT);
pinMode(mo6,OUTPUT);
pinMode(mo7,OUTPUT);
pinMode(mo8,OUTPUT);
pinMode(mi5,OUTPUT);
pinMode(mi6,OUTPUT);
pinMode(mi7,OUTPUT);
pinMode(mi8,OUTPUT);

Serial.begin(9600);
}
void loop() {
  digitalWrite(t1,LOW);
  delayMicroseconds(2);
  digitalWrite(t1,HIGH);
  delayMicroseconds(10);
  digitalWrite(t1,LOW);
  du = pulseIn(e1,HIGH);
  d= du/58;
  Serial.print("Distance1 = ");
  Serial.println(d);
  digitalWrite(t2,LOW);
  delayMicroseconds(2);
  digitalWrite(t2,HIGH);
  delayMicroseconds(10);
  digitalWrite(t2,LOW);
  du = pulseIn(e2,HIGH);
  d= du/58;
  Serial.print("Distance2 = ");
  Serial.println(d);
  digitalWrite(t3,LOW);
  delayMicroseconds(2);
  digitalWrite(t3,HIGH);
  delayMicroseconds(10);
  digitalWrite(t3,LOW);
  du = pulseIn(e3,HIGH);
  d= du/58;
  Serial.print("Distance3 = ");
  Serial.println(d);
  digitalWrite(t4,LOW);
  delayMicroseconds(2);
  digitalWrite(t4,HIGH);
  delayMicroseconds(10);
  digitalWrite(t4,LOW);
  du = pulseIn(e4,HIGH);
  d= du/58;
  Serial.print("Distance4 = ");
  Serial.println(d);
for(b=0;b<=255;b++)
{
  digitalWrite(mo1,HIGH);
  digitalWrite(mi1,LOW);
  digitalWrite(mo2,HIGH);
  digitalWrite(mi2,LOW);
  digitalWrite(mo3,HIGH);
  digitalWrite(mi3,LOW);
  digitalWrite(mo4,HIGH);
  digitalWrite(mi4,LOW);
  digitalWrite(mo5,HIGH);
  digitalWrite(mi5,LOW);
  digitalWrite(mo6,HIGH);
  digitalWrite(mi6,LOW);
  digitalWrite(mo7,HIGH);
  digitalWrite(mi7,LOW);
  digitalWrite(mo8,HIGH);
  digitalWrite(mi8,LOW);
  
  analogWrite(en1,b);  
  analogWrite(en2,0);
  analogWrite(en3,b);
  analogWrite(en4,0);

  delay(10);
}
delay(5000);
for(b=0;b<=255;b++)
{
  digitalWrite(mo1,LOW);
  digitalWrite(mi1,HIGH);
  digitalWrite(mo2,HIGH);
  digitalWrite(mi2,LOW);
  digitalWrite(mo3,LOW);
  digitalWrite(mi3,HIGH);
  digitalWrite(mo4,HIGH);
  digitalWrite(mi4,LOW);
  digitalWrite(mo5,LOW);
  digitalWrite(mi5,HIGH);
  digitalWrite(mo6,HIGH);
  digitalWrite(mi6,LOW);
  digitalWrite(mo7,LOW);
  digitalWrite(mi7,HIGH);
  digitalWrite(mo8,HIGH);
  digitalWrite(mi8,LOW);
  analogWrite(en1,b);  
  analogWrite(en2,0);
  analogWrite(en3,b);
  analogWrite(en4,0);
  delay(10);
}delay(5000);
for(a=0;a<=255;a++)
{
  digitalWrite(mo1,HIGH);
  digitalWrite(mi1,LOW);
  digitalWrite(mo2,HIGH);
  digitalWrite(mi2,LOW);
  digitalWrite(mo3,HIGH);
  digitalWrite(mi3,LOW);
  digitalWrite(mo4,HIGH);
  digitalWrite(mi4,LOW);
  digitalWrite(mo5,HIGH);
  digitalWrite(mi5,LOW);
  digitalWrite(mo6,HIGH);
  digitalWrite(mi6,LOW);
  digitalWrite(mo7,HIGH);
  digitalWrite(mi7,LOW);
  digitalWrite(mo8,HIGH);
  digitalWrite(mi8,LOW);
  analogWrite(en1,0);  
  analogWrite(en2,a);
  analogWrite(en3,0);
  analogWrite(en4,a);
  delay(10); 
}delay(5000);
for(a=0;a<=255;a++)
{
  digitalWrite(mo1,LOW);
  digitalWrite(mi1,HIGH);
  digitalWrite(mo2,LOW);
  digitalWrite(mi2,HIGH);
  digitalWrite(mo3,LOW);
  digitalWrite(mi3,HIGH);
  digitalWrite(mo4,LOW);
  digitalWrite(mi4,HIGH);
  digitalWrite(mo5,LOW);
  digitalWrite(mi5,HIGH);
  digitalWrite(mo6,HIGH);
  digitalWrite(mi6,LOW);
  digitalWrite(mo7,LOW);
  digitalWrite(mi7,HIGH);
  digitalWrite(mo8,HIGH);
  digitalWrite(mi8,LOW);
  analogWrite(en1,0);  
  analogWrite(en2,a);
  analogWrite(en3,0);
  analogWrite(en4,a);
  delay(10);
}delay(5000);
}
