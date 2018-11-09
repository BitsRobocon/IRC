#import evdev
from evdev import InputDevice,categorize,ecodes

#creates object 'gamepad' to store data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event0')

#prints out device info at start
print(gamepad)

#evdev takes care of polling the controller in loop
for event in gamepad.read_loop():
    print(categorize(event))
