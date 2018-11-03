import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

led1 = 3
led2 = 5

GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)

time_gap = float(raw_input("Please enter your time gap"))

try:
	while True:
		GPIO.output(led1,True)
		GPIO.output(led2,False)
		sleep(time_gap)
		GPIO.output(led1,False)
		GPIO.output(led2,True)
		sleep(time_gap)
except KeyboardInterrupt:
	GPIO.cleanup()
	print "\nAu revoir"

