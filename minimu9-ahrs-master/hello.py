import subprocess
import shlex
import time




process = subprocess.Popen(shlex.split("minimu9-ahrs --output euler"), stdout=subprocess.PIPE)
#time.sleep(5)


while True:

	output = process.stdout.readline()
	print "Now the angle is: "+ output.strip()[:6]


	

    