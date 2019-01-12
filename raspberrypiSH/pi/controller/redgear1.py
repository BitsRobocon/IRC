from evdev import InputDevice,categorize,ecodes
import  RPi.GPIO as GPIO
gamepad = InputDevice('/dev/input/event0')

#button codes
CA=304         #0,1
CB=305         #0,1
CY=308         #0,1
CX=307         #0,1
CR1=311        #0,1
CL1=310        #0,1
Cback=314      #0,1
Cstart=315     #0,1
Chome=316      #0,1
CL3=317        #0,1
CR3=318        #0,1
CR2=5          #0,255
CL2=2          #0,255
CLX=0          #-32768,32767
CLY=1          #-32768,32767 sign inverted
CRX=3          #-32768,32767
CRY=4          #-32768,32767 sign inverted
CH=16          #-1,0,1
CV=17          #-1,0,1 sign inverted

#GPIOPins
MRf=2
MRb=3
MRe=4
MLf=5
MLb=6
MLe=7

GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(MRf,GPIO.OUT)
GPIO.setup(MRb,GPIO.OUT)
GPIO.setup(MRe,GPIO.OUT)
GPIO.setup(MLf,GPIO.OUT)
GPIO.setup(MLb,GPIO.OUT)
GPIO.setup(MLe,GPIO.OUT)

Trx=0
Try=0
MRs=0
MLs=0

for event in gamepad.read_loop():
    if event.code is CRY:
       Try=-event.value/415
    if event.code is CRX:
       Trx=(event.value/365)/4
    MRs=Try-Trx
    MLs=Try+Trx
    MRo=GPIO.PWM(MRe,50)
    MLo=GPIO.PWM(MLe,50)
    if(MRs>=0):
       if(MRs>100):
         MRs=100
       GPIO.output(MRf,GPIO.HIGH)
       GPIO.output(MRb,GPIO.LOW)
       MRo.start(MRs)
    if(MRs<0):
       if(MRs<-100):
         MRs=-100
       GPIO.output(MRf,GPIO.LOW)
       GPIO.output(MRb,GPIO.HIGH)
       MRo.start(-MRs)
    if(MLs>=0):
       if(MLs>100):
         MLs=100
       GPIO.output(MLf,GPIO.HIGH)
       GPIO.output(MLb,GPIO.LOW)
       MLo.start(MLs)
    if(MLs<0):
       if(MLs<-100):
         MLs=-100
       GPIO.output(MLf,GPIO.LOW)
       GPIO.output(MLb,GPIO.HIGH)
       MLo.start(-MLs)
    print "LS= "+str(MLs)+"   RS= "+str(MRs)
