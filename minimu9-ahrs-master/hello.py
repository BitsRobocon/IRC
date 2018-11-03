import subprocess
import shlex
import time



process = subprocess.Popen(shlex.split("minimu9-ahrs --output euler"), stdout=subprocess.PIPE)


time.sleep(4)


print("Started")


for i in range(0,100):
	output = float(process.stdout.readline()[:6])
	
start = output


'''

if start > 90:
	while output >90 :
		print("turning"+str(output))
		output = float(process.stdout.readline()[:6])	#right

	while (output +180-start) < 90:
		print("turning"+str(output))
		output = float(process.stdout.readline()[:6])

else:

	while (output-start) < 90:
		print("turning"+str(output))
		output = float(process.stdout.readline()[:6])


'''

if start < 90:
	while output < 90 :
		print("turning"+str(output))
		output = float(process.stdout.readline()[:6])

	while (180 - output +start) < 90:
		print("turning"+str(output))
		output = float(process.stdout.readline()[:6])

else:

	while (start - output) < 90:
		print("turning"+str(output))
		output = float(process.stdout.readline()[:6])







print("Reached Position")	



	

    