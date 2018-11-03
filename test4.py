import RPi.GPIO as GPIO
from time import sleep

led = 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(led,GPIO.OUT)

pwm = GPIO.PWM(led,500)

pwm.start(0)

try:
	while True:
		for i in range(0,101,5):
			pwm.ChangeDutyCycle(i)
			sleep(0.1)
		for i in range(100,-1,-5):
			pwm.ChangeDutyCycle(i)
			sleep(0.1)
except KeyboardInterrupt:
	pwm.stop()
	GPIO.cleanup()
	print "Au Revoir"

