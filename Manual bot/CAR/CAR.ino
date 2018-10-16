#include <XBOXUSB.h>
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

byte LF=2;int LS=3; byte LB=4;byte RF=5;int RS=6;byte RB=7;
int x=0,y=0;
int rs=0,ls=0;

USB Usb;
XBOXUSB Xbox(&Usb);

void setup() {
  Serial.begin(115200);
  #if !defined(__MIPSEL__)
   while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
  #endif
   if (Usb.Init() == -1) {
    Serial.print(F("\r\nOSC did not start"));
    while (1); //halt
  }
  Serial.print(F("\r\nXBOX USB Library Started"));
  pinMode(LF,OUTPUT);
  pinMode(LS,OUTPUT);
  pinMode(LB,OUTPUT);
  pinMode(RF,OUTPUT);
  pinMode(RS,OUTPUT);
  pinMode(RB,OUTPUT);
  }
  void loop() {
   Usb.Task();
   if (Xbox.Xbox360Connected) {
    if (Xbox.getAnalogHat(RightHatX) != 0  || Xbox.getAnalogHat(RightHatY) != 0) {
      if (Xbox.getAnalogHat(RightHatX) != 0)
        x=map(Xbox.getAnalogHat(RightHatX),-32512,32512,-50,50);
        else x=0;
      if (Xbox.getAnalogHat(RightHatY) != 0)
        y=map(Xbox.getAnalogHat(RightHatY),-32512,32512,-200,200);
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
        analogWrite(RS,rs);
      }
       
      if(rs<0)
      {
        digitalWrite(RF,LOW);
        digitalWrite(RB,HIGH);
        analogWrite(RS,(-rs));
      }
       
      if(ls>=0)
      {
        digitalWrite(LF,HIGH);
        digitalWrite(LB,LOW);
        analogWrite(LS,ls);}
       
      if(rs<0)
      {
        digitalWrite(LF,LOW);
        digitalWrite(LB,HIGH);
        analogWrite(LS,(-ls));
      }   
    }
  delay(5);
}
