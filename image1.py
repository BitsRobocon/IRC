from picamera import PiCamera
from time import sleep


camera = PiCamera()

camera.annotate_text = "Team IRC"
camera.brightness = 50
camera.start_preview()
camera.rotation = 180
sleep(3)
camera.capture('/home/pi/Projects/intro/first.jpg')
camera.stop_preview()
#camera.start_recording('/home/pi/Projects/intro/second.h264')
#sleep(15)
#camera.stop_recording()
