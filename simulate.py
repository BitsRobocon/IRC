#import evdev
from evdev import InputDevice,categorize,ecodes

#creates object 'gamepad' to store data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event0')

#prints out device info at start
print(gamepad)

#button codes
A=304
B=305
Y=308
X=307
R1=311
L1=310
select=314
start=315
home=316
L3=317
R3=318
R2=5
L2=2
LX=0
LY=1
RX=3
RY=4

print(gamepad)

for event in gamepad.read_loop():
   if event.value!=0:
      if event.code is 4:
        print (-event.value/257)
