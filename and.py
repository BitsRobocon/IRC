import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT,initial=0)
GPIO.setup(5,GPIO.OUT,initial=0)
GPIO.setup(7,GPIO.IN,GPIO.PUD_DOWN)


try:
	while True:
		in1 = int(input("Enter pin 1: "))
		in2 = int(input("Enter pin 2: "))
		GPIO.output(3,in1)
		GPIO.output(5,in2)
		sleep(1)
		print(GPIO.input(7))
except KeyboardInterrupt:
	GPIO.cleanup()
	print("Bye")

