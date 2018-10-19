import RPi.GPIO as GPIO
import time
from pololu_drv8835_rpi import motors, MAX_SPEED
import smbus

Kp = 1
Kd = 0.8

Kp1 = 1.5

Kd1 = 1.0

distance_new_cell = 9

left_base = 80
right_base = 80

left_thresh = 27
right_thresh = 27

centre_thresh =25

wall_pid = 9.0

my_path = "SRLSLRSRSSRSRLSLRRLLRRL"

motor_spot_delay= 0.44

oldErrorP = 0

oldErrorP1 = 0

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47



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

	def MPU_Init():
	  	#write to sample rate register
	 	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	  
		#Write to power management register
		bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

		#Write to Configuration register
		bus.write_byte_data(Device_Address, CONFIG, 0)

		#Write to Gyro configuration register
		bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

		#Write to interrupt enable register
		bus.write_byte_data(Device_Address, INT_ENABLE, 1)

	def read_raw_data(addr):
		#Accelero and Gyro value are 16-bit
		high = bus.read_byte_data(Device_Address, addr)
		low = bus.read_byte_data(Device_Address, addr+1)

		#concatenate higher and lower value
		value = ((high << 8) | low)

		#to get signed value from mpu6050
		if(value > 32768):
		        value = value - 65536
		return value	

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

		for i in range(3):

			left_sensor = (calc_dist(PIN_TRIGGER_3,PIN_ECHO_3)+left_sensor)

			right_sensor = (calc_dist(PIN_TRIGGER_2,PIN_ECHO_2)+right_sensor)

		left_sensor = left_sensor/4
		
		right_sensor = right_sensor/4	


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

			#wall_pid = sensor_array[0] 
			
			while (sensor_array[0]< left_thresh and sensor_array[2]>right_thresh):

				sensor_array = mes_sense()

				error = side_PID_calc(sensor_array[0])

				#print(sensor_array)

				motor_control(-error)

				if (sensor_array[2]<right_thresh):
					time.sleep(0.35)
					sensor_array = mes_sense()




		elif wall == "right":

			#wall_pid = sensor_array[2]

			while (sensor_array[0]> left_thresh and sensor_array[2]<right_thresh):

				sensor_array = mes_sense()
				error = side_PID_calc(sensor_array[2])

				motor_control(error)

				if (sensor_array[0] < left_thresh ):
					time.sleep(0.35)
					sensor_array = mes_sense()

		elif wall=="no_wall":
			while (sensor_array[1]>13):
				#print(sensor_array[1])
				
				turn_motors(left_base,right_base)
				sensor_array = mes_sense()

				if (sensor_array[1]<15):
					break

		motors.setSpeeds(0,0)		

				



	i =0

	bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
	Device_Address = 0x68   # MPU6050 device address

	MPU_Init()

	while True:



		print "			I am going " + my_path[i]

		if my_path[i] == 'S':


			sensor_array = mes_sense()


			available_walls = check_available_walls()


			print ("Available walls are:" + available_walls)

			final_pid(available_walls)

			#print "New cell identified"

			


			while my_path[i+1] == 'S':	# Going straight if junction not required
				#print "Just keep going straight"
				print("Going straight!!!!")
				available_walls = check_available_walls()
				final_pid(available_walls)
				i=i+1

			'''	
			
			sensor_array = calc_dist(PIN_TRIGGER_1,PIN_ECHO_1)
											#now just adjusting into new cell
			initial_pos = sensor_array

			print "Inital Position is" + str(initial_pos)
			final_pos = sensor_array

			

			while ((initial_pos - final_pos < distance_new_cell)):


				turn_motors(left_base,right_base)
				sensor_array = calc_dist(PIN_TRIGGER_1,PIN_ECHO_1)

				final_pos = sensor_array

				print final_pos

				

			print "Final Position is" + str(final_pos)
			motors.setSpeeds(0,0) # Stopping motors in new cell
			'''

			turn_motors(left_base,right_base)
			time.sleep(0.2)

			motors.setSpeeds(0,0)

			

			print "New cell has been acheived"

		



			i=i+1		

		elif my_path[i] == 'R':

			yaw = 0

			turn_motors(60,-60)		# Initial spot turn

			while True:
				gyro_z = read_raw_data(GYRO_ZOUT_H)
				Gz = gyro_z/131.0
				yaw = yaw + Gz
				if yaw>100:
					break
				time.sleep(0.1)
			print ("My yaw is :" + str(yaw)	)


			motors.setSpeeds(0,0)

			#print "Turned right"

			#time.sleep(5)


			available_walls = check_available_walls()

			print ("Available walls are:" + available_walls)

			final_pid(available_walls)


			while my_path[i+1] == 'S':	# Going straight if junction not required
				available_walls = check_available_walls()
				print("Going straight!!!!")
				#print (available_walls)
				final_pid(available_walls)
				print ("Available walls are:" + available_walls)
				i=i+1
			'''
			sensor_array = mes_sense()
			
			initial_pos = sensor_array[1]	#now just adjusting into new cell
			final_pos = sensor_array[1]

			while (initial_pos - final_pos < distance_new_cell):

				turn_motors(left_base,right_base) # Just keep going straight
				sensor_array = mes_sense()

				final_pos = sensor_array[1]

			motors.setSpeeds(0,0) # Stopping motors in new cell	

			'''

			turn_motors(left_base,right_base)
			time.sleep(0.2)

			motors.setSpeeds(0,0)

			
			i=i+1


		elif my_path[i] == 'L':
			
			yaw = 0
			turn_motors(-60,60)

			while yaw > -(80):
				gyro_z = read_raw_data(GYRO_ZOUT_H)
				Gz = gyro_z/131.0
				yaw = yaw + Gz
				# Initial spot turn
				time.sleep(0.1)

			motors.setSpeeds(0,0)

			#time.sleep(4)

			sensor_array = mes_sense()

			available_walls = check_available_walls()	

			print ("Available walls are:" + available_walls)

			final_pid(available_walls)

			while my_path[i+1] == 'S':	# Going straight if junction not required
				print("Going straight!!!!")
				available_walls = check_available_walls()
				print ("Available walls are:" + available_walls)
				final_pid(available_walls)
				i=i+1

			sensor_array = mes_sense()

			initial_pos = sensor_array[1]	#now just adjusting into new cell
			final_pos = sensor_array[1]
			'''
			while (initial_pos - final_pos < distance_new_cell):

				turn_motors(left_base,right_base) # Just keep going straight
				sensor_array = mes_sense()

				final_pos = sensor_array[1]

			motors.setSpeeds(0,0) # Stopping motors in new cell
			'''

			turn_motors(left_base,right_base)
			time.sleep(0.2)

			motors.setSpeeds(0,0)

			i=i+1 



			


finally:
	motors.setSpeeds(0,0)		

