import RPi.GPIO as GPIO
import time

try:
      GPIO.setmode(GPIO.BCM)

      PIN_TRIGGER_1 = 18
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

      GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
      GPIO.output(PIN_TRIGGER_2, GPIO.LOW)
      GPIO.output(PIN_TRIGGER_3, GPIO.LOW)

      def calc_dist(PIN_TRIGGER,PIN_ECHO):
        #print "Calculating distance"

        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        return distance
        time.sleep(1)
      print "Waiting for Godot"

      time.sleep(2)
      while True:
        print str(calc_dist(PIN_TRIGGER_3,PIN_ECHO_3))+" "+str(calc_dist(PIN_TRIGGER_1,PIN_ECHO_1))+" "+str(calc_dist(PIN_TRIGGER_2,PIN_ECHO_2))
        time.sleep(0.1)
finally:
      GPIO.cleanup()
