import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

led = 7
switch = 11

GPIO.setup(led,GPIO.OUT)
GPIO.setup(switch,GPIO.IN,GPIO.PUD_UP)

try:
    while True:
		GPIO.output(led,not GPIO.input(switch))
except KeyboardInterrupt:
    GPIO.cleanup()
    print "Au Revoir"
