from evdev import InputDevice,categorize,ecodes
import  RPi.GPIO as GPIO
from pololu_drv8835_rpi import motors, MAX_SPEED
import RPi.GPIO as GPIO
import time
gamepad = InputDevice('/dev/input/event0')

GPIO.setmode(GPIO.BCM)

PIN_TRIGGER_1 = 18#PIN DEFINITION OF ULTRASOUND PINS
PIN_ECHO_1 = 27

PIN_TRIGGER_2 = 4
PIN_ECHO_2 = 17

PIN_TRIGGER_3 = 22
PIN_ECHO_3 = 23

GPIO.setup(PIN_TRIGGER_1, GPIO.OUT)
GPIO.setup(PIN_ECHO_1, GPIO.IN)
GPIO.setup(PIN_TRIGGER_2, GPIO.OUT)
GPIO.setup(PIN_ECHO_2, GPIO.IN)
GPIO.setup(PIN_TRIGGER_3, GPIO.OUT)
GPIO.setup(PIN_ECHO_3,GPIO.IN)

GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
GPIO.output(PIN_TRIGGER_2, GPIO.LOW)
GPIO.output(PIN_TRIGGER_3, GPIO.LOW)

motors.setSpeeds(0, 0)

def turn_motors(left_motor,right_motor):
    motors.motor1.setSpeed(left_motor)

    motors.motor2.setSpeed(right_motor)

def calc_dist(PIN_TRIGGER,PIN_ECHO):
    #print "Calculating distance"

    GPIO.output(PIN_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
      pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
      pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    return distance

def mes_sense():
  print "kk"
  front_sensor = calc_dist(PIN_TRIGGER_1,PIN_ECHO_1)
  #right_sensor = calc_dist(PIN_TRIGGER_2,PIN_ECHO_2)
  left_sensor = calc_dist(PIN_TRIGGER_3,PIN_ECHO_3)
  print "go"
  for i in range(3):

    left_sensor = (calc_dist(PIN_TRIGGER_3,PIN_ECHO_3)+left_sensor)
    
    #right_sensor = (calc_dist(PIN_TRIGGER_2,PIN_ECHO_2)+right_sensor)

  left_sensor = left_sensor/4
  print "go1"
  #right_sensor = right_sensor/4 


  sensor_array = [left_sensor,front_sensor]
  print sensor_array
  return sensor_array     

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

'''
GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(MRf,GPIO.OUT)
GPIO.setup(MRb,GPIO.OUT)
GPIO.setup(MRe,GPIO.OUT)
GPIO.setup(MLf,GPIO.OUT)
GPIO.setup(MLb,GPIO.OUT)
GPIO.setup(MLe,GPIO.OUT)
'''

Trx=0
Try=0
MRs=0
MLs=0
ultra=0
base_speed = 150
right_coef = 3
left_coef = 3
for event in gamepad.read_loop():
    turn_motors(0,0)
    if event.code is CRY:
       Try=-event.value/415
    if event.code is CRX:
       Trx=(event.value/365)/4
    if event.code is CR2:
       ultra=event.value   
       print ultra
    print "goat" 

    MRs=Try-Trx
    MLs=Try+Trx
    #MRo=GPIO.PWM(MRe,50)
    #MLo=GPIO.PWM(MLe,50)

    if(ultra>200):
       print mes_sense()

    elif(MRs>=50 and MLs >=50):
       if(MRs>100):
         MRs=100

       #GPIO.output(MRf,GPIO.HIGH)
       #GPIO.output(MRb,GPIO.LOW)
       turn_motors(int(base_speed + right_coef*MRs),int(base_speed + left_coef*MLs))
       print "forward"
       #MRo.start(MRs)
    elif(MRs<=-18 and MLs >=15 and MRs>=-30 and MLs <=30):
       if(MRs<-100):
         MRs=-100
       #GPIO.output(MRf,GPIO.LOW)
       #GPIO.output(MRb,GPIO.HIGH)
       turn_motors(base_speed,0)
       print "right"
       #MRo.start(-MRs)
    elif(MRs<=30 and MRs>=15 and MLs <=-15 and MLs >=-30 ):
       if(MRs<=18 and MLs >=18):
         MLs=100
       #GPIO.output(MLf,GPIO.HIGH)
       #GPIO.output(MLb,GPIO.LOW)
       turn_motors(0,base_speed)
       print "left"
       #MLo.start(MLs)
    elif(MRs<=-50 and  MLs <=-50):
       if(MRs>=18 and MLs <=18):
         MLs=-100
       #GPIO.output(MLf,GPIO.LOW)
       #GPIO.output(MLb,GPIO.HIGH)
       turn_motors(int(-base_speed + right_coef*MRs),int(-base_speed + left_coef*MLs))
       print "back"
       #MLo.start(-MLs)
    else:
        turn_motors(0,0)   
    print "LS= "+str(MLs)+"   RS= "+str(MRs)
