import RPi.GPIO as GPIO
import time
from pololu_drv8835_rpi import motors, MAX_SPEED

Kp = 1
Kd = 0.8

Kp1 = 1.5

Kd1 = 1.0

distance_new_cell = 9

left_base = 80+8
right_base = 80

left_thresh = 27
right_thresh = 27

centre_thresh =25

wall_pid = 9.0

pid_offset = 0

my_path = "SRLSLRSRSSR"

motor_spot_delay= 0.25

oldErrorP = 0

oldErrorP1 = 0 



try:

	motors.setSpeeds(0, 0)

	GPIO.setmode(GPIO.BCM)

	PIN_TRIGGER_1 = 18
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
		front_sensor = calc_dist(PIN_TRIGGER_1,PIN_ECHO_1)
		right_sensor = calc_dist(PIN_TRIGGER_2,PIN_ECHO_2)
		left_sensor = calc_dist(PIN_TRIGGER_3,PIN_ECHO_3)

			


		sensor_array = [left_sensor,front_sensor,right_sensor]

		return sensor_array	

	def PID_calc(sensor_array):

		global oldErrorP,Kp,Kd
			



		errorP = sensor_array[0] - sensor_array[2] 

		errorD = errorP - oldErrorP
		total_error = Kp*errorP + Kd*errorD

		oldErrorP = errorP

		return total_error

	def side_PID_calc(sensor):

		global oldErrorP1,Kp1,Kd1


		errorP = wall_pid - sensor
		errorD = errorP - oldErrorP1

		oldErrorP1 = errorP

		total_error = Kp1*errorP + Kd1*errorD


		return total_error 	

	def motor_control(error):

		global right_base,left_base

		right_motor_speed = right_base + error

		left_motor_speed = left_base - error

		motors.motor1.setSpeed(int(left_motor_speed))

		motors.motor2.setSpeed(int(right_motor_speed))

	def turn_motors(left_motor,right_motor):
			motors.motor1.setSpeed(left_motor)

			motors.motor2.setSpeed(right_motor)

	def check_available_walls():
			sensor_array = mes_sense()
			if (sensor_array[0]< left_thresh and sensor_array[2]<right_thresh):
				return "both"
			elif (sensor_array[0]< left_thresh and sensor_array[2]>right_thresh):
				return "left"	
			elif (sensor_array[0]> left_thresh and sensor_array[2]<right_thresh):
				return "right"
			elif (sensor_array[0]> left_thresh and sensor_array[2]>right_thresh):
				return "no_wall"

	def final_pid(wall):
		sensor_array = mes_sense()

		if wall == "both":

			while(sensor_array[0]< left_thresh and sensor_array[2]<right_thresh):

				sensor_array = mes_sense()
				error = PID_calc(sensor_array)

				motor_control(error)

		elif wall == "left":
			
			while (sensor_array[0]< left_thresh and sensor_array[2]>right_thresh):

				sensor_array = mes_sense()
				error = side_PID_calc(sensor_array[0])

				motor_control(-error)

		elif wall == "right":

			while (sensor_array[0]> left_thresh and sensor_array[2]<right_thresh):

				sensor_array = mes_sense()
				error = side_PID_calc(sensor_array[2])

				motor_control(error)

		elif wall=="no_wall":
			while (sensor_array[1]>13):
				#print(sensor_array[1])
				
				turn_motors(left_base,right_base)
				sensor_array = mes_sense()

				if (sensor_array[1]<10):
					break

		motors.setSpeeds(0,0)		

				



	i =0

	while True:
		'''
		sensor_array = mes_sense()

		if ((sensor_array[0] - sensor_array[2]) < (-7)):
			turn_motors(left_base,0)
			time.sleep(0.2)
			turn_motors(0,right_base)
			time.sleep(0.2)

		elif ((sensor_array[0] - sensor_array[2]) > 7 ):
			turn_motors(0,right_base)
			time.sleep(0.2)
			turn_motors(left_base,0)
			time.sleep(0.2)

		else:

			error = PID_calc(sensor_array)
			motor_control(error)
		'''	
		#time.sleep(0.4)
		#print error
		sensor_array = mes_sense()
		error = side_PID_calc(sensor_array[0])
		motor_control(-error)
		

		

			

			


finally:
	motors.setSpeeds(0,0)		

