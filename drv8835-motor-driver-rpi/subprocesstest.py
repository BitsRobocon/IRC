import subprocess
import shlex

process=subprocess.Popen(shlex.split("minimu9-ahrs --output euler"),stdout=subprocess.PIPE)

