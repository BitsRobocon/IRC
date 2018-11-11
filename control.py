from evdev import InputDevice,categorize,ecodes
import  RPi.GPIO as GPIO
gamepad = InputDevice('/dev/input/event0')

#button codes
A=304         #0,1
B=305         #0,1
Y=308         #0,1
X=307         #0,1
R1=311        #0,1
L1=310        #0,1
select=314    #0,1
start=315     #0,1
home=316      #0,1
L3=317        #0,1
R3=318        #0,1
R2=5          #0,255
L2=2          #0,255
LX=0          #-32768,32767 
LY=1          #-32768,32767 sign inverted
RY=4          #-32768,32767 sign inverted
RX=3          #-32768,32767
V=17          #-1,0,1 sign inverted
H=16          #-1,0,1

#GPIOPins
r1=2
r2=3
rs=4
l1=5
l2=6
ls=7

GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(r1,GPIO.OUT)
GPIO.setup(r2,GPIO.OUT)
GPIO.setup(rs,GPIO.OUT)
GPIO.setup(l1,GPIO.OUT)
GPIO.setup(l2,GPIO.OUT)
GPIO.setup(ls,GPIO.OUT)

rx=0
ry=0
rms=0
lms=0

for event in gamepad.read_loop():
      if event.code is RY:
       ry=-event.value/415
      if event.code is RX:
       rx=(event.value/365)/4
      rms=ry-rx
      lms=ry+rx
      rm=GPIO.PWM(rs,50)
      lm=GPIO.PWM(ls,50)
      if(rms>=0):
       GPIO.output(r1,GPIO.HIGH)
       GPIO.output(r2,GPIO.LOW)
       rm.start(rms)
      if(rms<0):
       GPIO.output(r1,GPIO.LOW)
       GPIO.output(r2,GPIO.HIGH)
       rm.start(-rms)
      if(lms>=0):
       GPIO.output(l1,GPIO.HIGH)
       GPIO.output(l2,GPIO.LOW)
       lm.start(lms)
      if(lms<0):
       GPIO.output(l1,GPIO.LOW)
       GPIO.output(l2,GPIO.HIGH)
       lm.start(-lms)
      print "LS= "+str(lms)+"   RS= "+str(rms)
