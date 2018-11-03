import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

led = 7
switch = 11
ledState = False

GPIO.setup(led,GPIO.OUT)
GPIO.setup(switch,GPIO.IN,GPIO.PUD_UP)

GPIO.output(led,ledState)

def myState(channel):
	global ledState,led
	ledState = not ledState
	print "The state is {}".format("On" if ledState else "Off")
	GPIO.output(led,ledState)

GPIO.add_event_detect(switch,GPIO.BOTH,myState,600)

try:
	while True:
		sleep(0.5)
except KeyboardInterrupt:
	GPIO.cleanup()
	print "Au revoir"
