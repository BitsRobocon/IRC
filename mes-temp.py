import os

temp = os.popen("vcgencmd measure_temp").readline().replace("temp=","The temperature is: ").replace("\n","")

print temp
