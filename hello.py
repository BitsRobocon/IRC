import subprocess
import shlex
import time




process = subprocess.Popen(shlex.split("minimu9-ahrs --output euler"), stdout=subprocess.PIPE)


print("Going forward")
start = time.time()
while True:
	output = process.stdout.readline().strip()[:6]

	if (time.time() - start) > 5:
		break




while True:

	print("turning")



	output = process.stdout.readline().strip()[:6]

	print "Now the angle is: "+ output

	if float(output)>75:
		print "REACHED!!!"
		break

	

    