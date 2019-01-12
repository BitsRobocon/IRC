#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from pololu_drv8835_rpi import motors, MAX_SPEED
import subprocess
import serial
import sys
import pyzbar.pyzbar as pyzbar
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import os

Kp = 10
Kd = 2#for both walls together

Kp1 = 10
#for one wall
Kd1 = 1.2

error_limit = 29

turn_speed = 90

distance_new_cell = 9.5#distance to stop from wall

left_base =72#base speed of motors
right_base = 67

jhatka_speed = 90

left_turn_angle = 63.00

right_turn_angle = 60.00

normal_blocks = 0

qr_block_flag = 0

qr_blocks = 0 



left_thresh = 17#reference distance from two sides
right_thresh = 17

centre_thresh =28.5#reference distance from front

wall_pid = 9.5# threshold for pid

both_wall_pid = 0 

my_path =  ""#"SRLSLRSSRSSRSRLSLRRLLRRL"#path



oldErrorP = 0

oldErrorP1 = 0

forward_delay = 0.20

block_lift_delay = 2

turn_active = False

threshArea = [20000.0,200000.0]

camera= PiCamera()
camera.resolution = (640,480) 						#Setting up picam
rawCapture= PiRGBArray(camera, size=(640,480))

color = {"Hue":[40,182],"Sat":[114,255],"Val":[34,255],"name":"something"}

simple_paths = {"LBR":"B","LBS":"R","LBL":"S","SBL":"R","SBS":"B","RBL":"B"}


try:

	motors.setSpeeds(0, 0)

	GPIO.setmode(GPIO.BCM)

	PIN_TRIGGER_1 = 16#PIN DEFINITION OF ULTRASOUND PINS
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
	GPIO.setup(18, GPIO.OUT)
	GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#Reset_Pin
	GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#Start_Pin
	GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#Start_Map_again

	reset= 25
	start= 8
	start_map=7

	servo = GPIO.PWM(18, 50)

	servo.start(7.5)

	servo.ChangeDutyCycle(12.5) # turn towards 180 degree(Left)

	Led_array = [19,20,21,26]

	for i in Led_array:
		GPIO.setup(i,GPIO.OUT)
		GPIO.output(i,GPIO.LOW)

	GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
	GPIO.output(PIN_TRIGGER_2, GPIO.LOW)
	GPIO.output(PIN_TRIGGER_3, GPIO.LOW)


	def reset_callback(channel):
		camera.stop_preview()
		camera.close()
		turn_motors(0,0)
		print("Reseting")
		os.execv(__file__, sys.argv)

	GPIO.add_event_detect(reset,GPIO.FALLING,callback=reset_callback)	


	def check_block(): #Image Processing
		global color
		camera.capture(rawCapture, format= "bgr")
		frame = rawCapture.array

		decodedObjects = pyzbar.decode(frame)

		if len(decodedObjects)>0:
		    for obj in decodedObjects:
		        print('Type : ', obj.type)
		        print('Data : ', obj.data,'\n')
		        data = int(obj.data)
		        if data = 1:
		        	Led_control([1,0,0,0])
		        elif data=2:
		        	Led_control([0,1,0,0])
		        elif data=3:
		        	Led_control([0,0,1,0])
		        elif data=4:
		        	Led_control([0,0,0,1])
		        rawCapture.truncate(0)
		        return "QR"
		 
		else:
		    frameBGR = cv2.GaussianBlur(frame, (7, 7), 0)
		   
		    hsv = cv2.cvtColor(frameBGR, cv2.COLOR_BGR2HSV)





		    colorLow = np.array([color["Hue"][0],color["Sat"][0],color["Val"][0]])
		    colorHigh = np.array([color["Hue"][1],color["Sat"][1],color["Val"][1]])
		    mask = cv2.inRange(hsv, colorLow, colorHigh)
		    # Show the first mask
		    #cv2.imshow('mask-plain', mask)
		    #cv2.waitKey(0)
		    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
		    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
		    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
		     
		    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		    cv2.drawContours(frame, contours, -1, (0,255,0), 3)


		    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]

		    if len(contour_sizes) >0:

		        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
		        cv2.drawContours(frame, biggest_contour, -1, (0,255,0), 3)


		        biggest_contour_area = cv2.contourArea(biggest_contour)
		        
		        if (biggest_contour_area > threshArea[0]) and (biggest_contour_area < threshArea[1]):
		            #blockDetected = True
		            #print (color["name"] + "found!!" + str(cv2.contourArea(biggest_contour)))
		            rawCapture.truncate(0)
		            return "Normal"

		            cv2.imwrite('RESULT.jpg',mask)
		        
		        

		        #print(cv2.contourArea(biggest_contour))
		    else :
		        #print("Patrao Kai Na")
		        rawCapture.truncate(0)
		        return False
		         
		    
		rawCapture.truncate(0)



	def calc_dist(PIN_TRIGGER,PIN_ECHO):
		#print "Calculating distance"

		#GPIO.output (PIN_TRIGGER,GPIO.LOW)                                 
		#time.sleep (0.00005)

		GPIO.output(PIN_TRIGGER, GPIO.HIGH)

		time.sleep(0.00001)

		GPIO.output(PIN_TRIGGER, GPIO.LOW)

		intial_time = time.time()
		pulse_start_time = intial_time

		while GPIO.input(PIN_ECHO)==0:
		  pulse_start_time = time.time()
		  if pulse_start_time - intial_time > 0.02:
		  	return 0.0

		pulse_end_time = time.time()
		while GPIO.input(PIN_ECHO)==1:
		  pulse_end_time = time.time()
		  if pulse_end_time - pulse_start_time > 0.02:
		    GPIO.setup(PIN_ECHO, GPIO.OUT)
		    GPIO.output(PIN_ECHO, GPIO.LOW)
		    time.sleep(0.00001)
		    GPIO.setup(PIN_ECHO, GPIO.IN)

		    return 0.0

		pulse_duration = pulse_end_time - pulse_start_time
		distance = round(pulse_duration * 17150, 2)
		return distance

	def mes_sense():
		left_sensor = calc_dist(PIN_TRIGGER_1,PIN_ECHO_1)
		right_sensor = calc_dist(PIN_TRIGGER_2,PIN_ECHO_2)
		front_sensor = calc_dist(PIN_TRIGGER_3,PIN_ECHO_3)

		for i in range(5):

			left_sensor = (calc_dist(PIN_TRIGGER_1,PIN_ECHO_1)+left_sensor)
			front_sensor = (calc_dist(PIN_TRIGGER_3,PIN_ECHO_3)+front_sensor)

			right_sensor = (calc_dist(PIN_TRIGGER_2,PIN_ECHO_2)+right_sensor)

		front_sensor = front_sensor/6

		left_sensor = left_sensor/6
		
		right_sensor = right_sensor/6	


		sensor_array = [left_sensor,front_sensor,right_sensor]
		print (sensor_array)
		return sensor_array	

	def block_action():
		global normal_blocks,qr_block_flag,qr_blocks
		servo.ChangeDutyCycle(7.8)  # turn towards 90 degree(Front)

		if check_block()=="Normal":
			if qr_block_flag==1 and normal_blocks==1:
				while check_block()=="Normal":
					print("Normal block found(Qr already!)")
				spot_back()

			else:
				while check_block()=="Normal":
					print("Normal block found")
					
			normal_blocks = normal_blocks + 1
			return True

		elif check_block()=="QR":
			if normal_blocks == 2:
				if qr_blocks==2:
					global my_path
					my_path = "S" + my_path
					print("The final path is " + my_path)
					fo = open("path.txt","w")
					fo.write(my_path)
					fo.close() 
					#switch required
					subprocess.call(["python","wall_follower_head2.py"]) 	#Calling the main code
				else:	
					qr_blocks=qr_blocks+1
					normal_blocks=0
					qr_block_flag=0	

			else:
				qr_block_flag=1
			return True	

			
		else:
			return False			
				
		servo.ChangeDutyCycle(12.5)  # turn towards 90 degree(Left)		

			

	def PID_calc(sensor_array):

		global oldErrorP,Kp,Kd

		errorP = sensor_array[0] - sensor_array[2]	- both_wall_pid
		errorD = errorP - oldErrorP
		total_error = Kp*errorP + Kd*errorD
		
		if total_error > error_limit:
			total_error= error_limit
		if total_error < -error_limit:
			total_error = -error_limit		
		#print(total_error)
		
		oldErrorP = errorP

		return total_error

	def side_PID_calc(sensor):
		global oldErrorP1,Kp1,Kd1


		errorP = wall_pid - sensor
		errorD = errorP - oldErrorP1

		oldErrorP1 = errorP

		total_error = Kp1*errorP + Kd1*errorD
		
		if total_error > error_limit:
			total_error= error_limit
		if total_error < -error_limit:
			total_error = -error_limit
		#print(total_error)
	
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

	
	def spot_right():
		ser.flushInput()
		start=float(ser.readline())
		output = start
		turn_motors(turn_speed,-turn_speed)

		if start < (-180 + right_turn_angle):
			while output  < 0 :
				#print("Acheiving +")
				ser.flushInput()
				output=float(ser.readline())
				#print(output)	#right

			while (360 - output +start) < right_turn_angle:
				#print ("Acheiving -")
				ser.flushInput()
				output=float(ser.readline())
				#print(output)

		else:

			if start >0 :
				while(output<0):
					#print ("correcting")
					ser.flushInput()
					output=float(ser.readline())
					#print(output)


			while (start-output) < right_turn_angle:
				#print ("Normal")
				ser.flushInput()
				output=float(ser.readline())
				#print(output)
		print('Turned right')
		turn_motors(0,0)

		block_action()
		
								


	def spot_left():
		ser.flushInput()
		start = float(ser.readline())
		output=start
		turn_motors(-turn_speed,turn_speed)
				

		if start > (180 -left_turn_angle):
			while output > 0:
				#print ("Acheiving +")
				ser.flushInput()
				output=float(ser.readline())
				#print(output)

			while (360 + output -start) < left_turn_angle:
				#print ("Acheiving -")
				ser.flushInput()
				output=float(ser.readline())
				#print(output)

		else:

			if start <0 :
				while(output>0):
					#print ("correcting")
					ser.flushInput()
					output=float(ser.readline())
					#print(output)

			while (output - start) < left_turn_angle:
				#print ("Normal")
				ser.flushInput()
				output=float(ser.readline())
				#print(output)
		print('Turned left')
		turn_motors(0,0)
		block_action()		
						

	def new_cell_adjust():
		sensor_array = mes_sense()

		if sensor_array[1] < centre_thresh:
			print ("Going for the wall")
			'''
			available_walls = check_available_walls()
			final_pid(available_walls,distance_new_cell)
			'''
			while sensor_array[1] > distance_new_cell:
				turn_motors(left_base,right_base)
				sensor_array = mes_sense()
		else:
			turn_motors(left_base+jhatka_speed,right_base+jhatka_speed)
			time.sleep(forward_delay)
			print("JHATKA!")				


	def decide_turn(turn):
		global turn_active,my_path
		if turn=="L":
			print("Decide:L")
			new_cell_adjust()
			spot_left()
			turn_motors(0,0)
			turn_active = True

		elif turn=="S":
			print("Decide:S")
			return 

		elif turn=="R":
			print("Decide:R")
			new_cell_adjust()
			spot_right()
			turn_active = True
			turn_motors(0,0)

		elif turn=="B":
			print("Decide:B")
			spot_right()
			spot_right()
			turn_motors(0,0)
			my_path = my_path[:len(my_path)-2]+"B"
			time.sleep(3)			




	def check_path():
			sensor_array = mes_sense()
			if (sensor_array[0]> left_thresh):
				return "L"

			elif (sensor_array[1] > distance_new_cell):
				return "S"	

			elif (sensor_array[2] > right_thresh):
				return "R"	

			else:
				return "B"


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
		global wall_pid,distance_new_cell,both_wall_pid
		sensor_array = mes_sense()

		

		if wall=="both":

			both_wall_pid = sensor_array[0] - sensor_array[2]


				
			while (sensor_array[0]< left_thresh and sensor_array[2]<right_thresh):

				sensor_array = mes_sense()

				if sensor_array[1] < distance_new_cell:
					if block_action():
						 simplify_flag = False
					else:
						break	

				error = PID_calc(sensor_array)

				motor_control(error)

				



				
			print("Done with both_wall pid")

		elif wall=="left":

			wall_pid = sensor_array[0] 
				
			while (sensor_array[0]< left_thresh and sensor_array[1] > distance_new_cell and sensor_array[2]>right_thresh):

				sensor_array = mes_sense()
				error = side_PID_calc(sensor_array[0])
				motor_control(-error)

				
				
				if (sensor_array[2]<right_thresh):
					time.sleep(0.2)
					sensor_array = mes_sense()
				
			print("Done with left_wall pid")

		elif wall == "right":

				wall_pid = sensor_array[2]

				while (sensor_array[0]> left_thresh and sensor_array[1] > distance_new_cell and sensor_array[2]<right_thresh):

					sensor_array = mes_sense()

					error = side_PID_calc(sensor_array[2])
					motor_control(error)
					
					if (sensor_array[0] < left_thresh ):
						time.sleep(0.2)
						sensor_array = mes_sense()	

		elif wall=="no_wall":

			while(sensor_array[0]>left_thresh and sensor_array[1] > distance_new_cell and sensor_array[2]>right_thresh):
				sensor_array = mes_sense()
				turn_motors(left_base,right_base)

				if (sensor_array[0] < left_thresh ):
						time.sleep(0.2)
						sensor_array = mes_sense()

				if (sensor_array[2]<right_thresh):
					time.sleep(0.2)
					sensor_array = mes_sense()				


		turn_motors(0,0)

	def Led_control(control_array):
		global Led_array
		for i in range(4):
			GPIO.output(Led_array[i],control_array[i])

	def simplify_path(my_array):
		global simple_paths,simplify_flag


		length = len(my_array)

		if length<3 or my_array[length-2]!="B":
			return my_array

		else:
			if simplify_flag:
				for i in simple_paths:
					if my_array[length-3:length] == i:
						my_array = my_array[:length-3] + simple_paths[i]
						return my_array	
			else:
				simplify_flag=True 
				return my_array				


	def startup():

		while GPIO.input(start) == GPIO.HIGH:
			print("Waiting for the start")
		wall = check_available_walls()

		if wall == "both":

			while True:

				sensor_array = mes_sense()
				error = PID_calc(sensor_array)

				print (error)
				

				if error > 25:
					Led_control([0,0,1,1])

				elif error > 5:	 
					Led_control([0,1,1,1])

				elif error < -25:
					Led_control([1,1,0,0])

				elif error < -5:
					Led_control([1,1,1,0])

				else:
					Led_control([1,1,1,1])
					time.sleep(2)
					Led_control([0,0,0,0])
					#sys.exit("Jal Gaya")
					return
				
			
		elif wall == "left":

				
			print("Done with left_wall pid")		
				



		elif wall == "right":
			pass
							

		elif wall=="no_wall":
			pass	


				
	i =0
	
	startup()

	ser=serial.Serial("/dev/ttyUSB0",9600)
	ser.baudrate=9600

	start_t = time.time()

	while (time.time()-start_t < 9):

		Led_control([1,1,1,1])
		time.sleep(0.2)
		Led_control([0,0,0,0])
		time.sleep(0.2)
	Led_control([0,0,0,0])	

	camera.start_preview()
	#ser.flushInput()
	#start_pos = float(ser.readline())

	GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
	GPIO.output(PIN_TRIGGER_2, GPIO.LOW)
	GPIO.output(PIN_TRIGGER_3, GPIO.LOW)

	

	while True:


		wall = check_available_walls()
		final_pid(wall)

		present_path = check_path()

		wall = check_available_walls()

		print(wall)

		if present_path=='S' and turn_active and wall!="both":
			turn_active=False
		else:	
			turn_active=False
			my_path = my_path + present_path
		
		decide_turn(present_path)

		my_path = simplify_path(my_path)	

		print(my_path)

		#input("Should I?")
		



finally:
	global my_path
	my_path = "S" + my_path
	print("The final path is " + my_path)
	fo = open("path.txt","w")
	fo.write(my_path)
	fo.close() 
	motors.setSpeeds(0,0)		

