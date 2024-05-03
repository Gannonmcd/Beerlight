from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
gatepin = 11
GPIO.setup(gatepin, GPIO.OUT)

def TurnOn():
    GPIO.output(gatepin, 1)
    return "Turned On"

def TurnOff():
    GPIO.output(gatepin, 0)
    return "Turned Off"

def Flash(flashes=10, time_interval=0.25, endState=1):
    for flash in range(flashes):
        GPIO.output(gatepin, 1)
        time.sleep(time_interval)
        GPIO.output(gatepin, 0)
        time.sleep(time_interval)
        if (flash == flashes - 1) and endState:
            GPIO.output(gatepin, 1)
    return f"Flashed {flashes} times"

@app.route('/on', methods=['GET'])
def turn_on():
    return TurnOn()

@app.route('/off', methods=['GET'])
def turn_off():
    return TurnOff()

@app.route('/flash', methods=['GET'])
def flash():
    flashes = request.args.get('flashes', default=10, type=int)
    time_interval = request.args.get('time_interval', default=0.25, type=float)
    endState = request.args.get('endState', default=1, type=int)
    return Flash(flashes, time_interval, endState)

@app.route('/')
def index():
    return '''
    <h1>GPIO Control</h1>
    <p><a href="/on">Turn On</a></p>
    <p><a href="/off">Turn Off</a></p>
    <p><a href="/flash">Flash</a></p>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
