#include <XBOXUSB.h>
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>
#include <Servo.h>

byte LF=18;//orange
byte LS=2; //yellow
byte LSB=3; //yellow-black
byte LB=17;//green

byte RF=15;//grey
byte RS=4;//purple
byte RSB=5;//purple-black
byte RB=14;//blue

byte shootF=22;//blue
byte shootS=24;//green
byte shootB=26;//yellow

byte aim=30;

int x=0,y=0,c=0,o=0;

int rs=0,ls=0;

int armd=0;int handd=150;int gripd=0;

USB Usb;
XBOXUSB Xbox(&Usb);

Servo arm1;
Servo arm2;
Servo hand1;
Servo hand2;
Servo grip;
Servo reload;

void setup() {
  Serial.begin(115200);
  
  #if !defined(__MIPSEL__)
   while (!Serial);
  #endif
  if (Usb.Init() == -1) {
    Serial.print(F("\r\nOSC did not start"));
    while (1); //halt
  }

  arm1.attach(6);//right-increase is up
  arm2.attach(21);
  hand1.attach(7);//right-increase is up
  hand2.attach(20);//left-increase is down
  grip.attach(8);//increase is inside
  reload.attach(19);

  pinMode(shootF,OUTPUT);
  pinMode(shootS,OUTPUT);
  pinMode(shootB,OUTPUT);
  
  pinMode(LF,OUTPUT);
  pinMode(LS,OUTPUT);
  pinMode(LSB,OUTPUT);
  pinMode(LB,OUTPUT);
  pinMode(RF,OUTPUT);
  pinMode(RS,OUTPUT);
  pinMode(RSB,OUTPUT);
  pinMode(RB,OUTPUT);
 
  pinMode(aim,OUTPUT);

  arm1.write(armd);
  arm2.write(180-armd);
  hand1.write(handd);
  hand2.write(180-handd);
  grip.write(gripd);
  }

  void motors(){
    if (Xbox.getAnalogHat(LeftHatX) != 0  || Xbox.getAnalogHat(LeftHatY) != 0) {
      if (Xbox.getAnalogHat(LeftHatX) != 0)
        x=map(Xbox.getAnalogHat(LeftHatX),-32512,32512,-50,50);
      else x=0;
      if (Xbox.getAnalogHat(LeftHatY) != 0)
        y=map(Xbox.getAnalogHat(LeftHatY),-32512,32512,-200,200);
      else y=0;
      }
      else
      {
        x=0;y=0;
      }
      rs=y-x;
      ls=y+x;
      if(rs>=0)
      {
        digitalWrite(RF,HIGH);
        digitalWrite(RB,LOW);
        if(rs<20){
        analogWrite(RS,0);
        analogWrite(RSB,0);
        }else{
        analogWrite(RS,map(rs,20,255,38,255));
        analogWrite(RSB,rs);
      }
      }
       
      if(rs<0)
      {
        digitalWrite(RF,LOW);
        digitalWrite(RB,HIGH);
        if(rs>-20){
        analogWrite(RS,0);
        analogWrite(RSB,0);
        }else
        analogWrite(RS,-map(rs,-255,-20,-255,-32));
        analogWrite(RSB,(-rs));
      }
       
      if(ls>=0)
      {
        digitalWrite(LF,HIGH);
        digitalWrite(LB,LOW);
        if(ls<20){
        analogWrite(LSB,0);
        analogWrite(LS,0);
        }
        else
        {
        analogWrite(LSB,map(ls,20,255,22,255));
        analogWrite(LS,ls);
        }
      }
       
      if(ls<0)
      {
        digitalWrite(LF,LOW);
        digitalWrite(LB,HIGH);
        if(ls>-20){
          analogWrite(LS,0);
          analogWrite(LSB,0);
        }        
        else
        analogWrite(LSB,-map(ls,-255,-20,-255,-23));
        analogWrite(LS,(-ls));
      }
      Serial.print(ls);
      Serial.print("   ");
      Serial.println(rs);
  }

  void servos()
  {
    if ((Xbox.getAnalogHat(RightHatX) != 0)||(Xbox.getAnalogHat(RightHatY) != 0)||(Xbox.getButtonPress(L2) !=0)||(Xbox.getButtonPress(R2) !=0)){
     if (Xbox.getAnalogHat(RightHatX) != 0) 
        x=map(Xbox.getAnalogHat(RightHatX),-32512,32512,-3,3);
     else x=0;
     if (Xbox.getAnalogHat(RightHatY) != 0)
        y=map(Xbox.getAnalogHat(RightHatY),-32512,32512,-2,2);
     else y=0;
     if(Xbox.getButtonPress(L2) !=0)
      c=map(Xbox.getButtonPress(L2),0,255,0,3);
     else  c=0;
     if(Xbox.getButtonPress(R2) !=0)
      o=map(Xbox.getButtonPress(R2),0,255,0,3);
     else  o=0;
     
     armd=armd+y;
     handd=handd+x;
     gripd=gripd+c-o;
     
     armd=constrain(armd,0,90);
     handd=constrain(handd,0,180);
     gripd=constrain(gripd,0,180);
     
     arm1.write(armd);
     arm2.write(180-armd);
     hand1.write(handd);
     hand2.write(180-handd);
     grip.write(gripd);
     delay(50);
    }  
  }
  
  void loop() {
   Usb.Task();
   
   if (Xbox.Xbox360Connected) {
    Xbox.setRumbleOn(0,0);
       motors();
       servos();
       
     if (Xbox.getButtonClick(A)){
      digitalWrite(shootF,HIGH);
      digitalWrite(shootS,HIGH);
      digitalWrite(shootB,LOW);
     }
     if(Xbox.getButtonClick(B)){
      digitalWrite(shootF,LOW);
      digitalWrite(shootS,LOW);
      digitalWrite(shootB,LOW);
     }
     if (Xbox.getButtonClick(X))
      reload.write(100);
     if (Xbox.getButtonClick(Y))
      reload.write(30);
      
     if (Xbox.getButtonClick(L1))
     digitalWrite(aim,HIGH);
     if (Xbox.getButtonClick(R1))
     digitalWrite(aim,LOW);
     
    }
  delay(5);
}
