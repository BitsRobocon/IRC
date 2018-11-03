import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(5,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)

try:
    while True:
		GPIO.output(5,True)
		GPIO.output(3,False)
except KeyboardInterrupt:
    GPIO.cleanup()
    print "Exiting..."
