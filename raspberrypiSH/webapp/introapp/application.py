
from flask import Flask,render_template,request,redirect,url_for
import RPi.GPIO as GPIO
from time import sleep
import json

GPIO.setmode(GPIO.BOARD)

led = 7

GPIO.setup(led,GPIO.OUT)

pwm = GPIO.PWM(led,0.5)

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/gpio", methods=["POST"])
def gpio():
	global pwm
	pwm.start(0)
	data = request.get_json()
	if not data == None:
		data = {'state':data['state']}
	else:
		data={}
	if request.form.get('state') == 'On' or data.get('state')== 'On':
		pwm.ChangeDutyCycle(100)
		print("We have on")
	elif request.form.get('state') == 'Off':
		pwm.ChangeDutyCycle(0)
		print("We have off")
	elif request.form.get('state') == 'Blink':
		pwm.ChangeDutyCycle(50)
	return redirect(url_for('index'))
