 byte TF=8;int TS=9;byte TB=10;

void setup() {
  pinMode(TF,OUTPUT);pinMode(TS,OUTPUT);pinMode(TB,OUTPUT);
}

void loop() {
  for(int y=-255;y<256;y=y+5)
  {
  if(y>=0)
      {
        digitalWrite(TF,HIGH);
        digitalWrite(TB,LOW);
       }
       
      if(y<0)
      {
        digitalWrite(TF,LOW);
        digitalWrite(TB,HIGH);
      }
     
      

                                                 analogWrite(TS,y);
                                                 Serial.println(y);
                                                 delay(100);
}
}
