import subprocess
output = subprocess.check_output('minimu9-ahrs --output euler'.split())
print(output)
