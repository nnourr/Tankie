from flask import Flask, render_template, url_for, request, Response
from gpiozero import Motor
import RPi.GPIO as GPIO
import os

class Motor:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7,GPIO.OUT)
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(13,GPIO.OUT)
        GPIO.setup(15,GPIO.OUT)
    
    def forward(self):
        GPIO.output(7,True)
        GPIO.output(11,False)
        GPIO.output(13,True)
        GPIO.output(15,False)
    def backward(self):
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,False)
        GPIO.output(15,True)
    def right(self):
        GPIO.output(7,False)
        GPIO.output(11,True)
        GPIO.output(13,True)
        GPIO.output(15,False)
    def left(self):
        GPIO.output(7,True)
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,True)
    def stop(self):
        GPIO.output(7,False)
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,False) 

app = Flask(__name__)

moving = False
speed = 1

control = Motor()

authenticated = False

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forward', methods=['GET', 'POST'])
def forward():
    #motor go forward
    #moving = True
    if authenticated == True:
        global moving
        control.forward()
        moving = True
        return "200"
    else:
        return "401"

@app.route('/backward', methods=['GET', 'POST'])
def backward():
    #motor go forward
    #moving = True
    if authenticated == True:
        global moving
        control.backward()
        moving = True
        return "200"
    else:
        return "401"

@app.route('/left', methods=['GET', 'POST'])
def left():
    #motor go forward
    #moving = True
    if authenticated == True:
        global moving
        control.left()
        moving = True
        return "200"
    else:
        return "401"

@app.route('/right', methods=['GET', 'POST'])
def right():
    #motor go forward
    #moving = True
    if authenticated == True:
        global moving
        control.right()
        moving = True
        return "200"
    else:
        return "401"

@app.route("/release", methods=['GET', 'POST'])
def stop():
    if authenticated == True:
        global moving
        if (moving == True):
            control.stop()
            moving = False
        return "200"
    else:
        return "401"

@app.route("/auth", methods=['GET','POST'])
def checkAuth():
    print(request.form)
    if request.form["password"] == os.environ.get('PASSWORD'):
        global authenticated
        authenticated = True
        return "True"
    else:
        return "False"

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")