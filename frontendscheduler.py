from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

logger=logging.getLogger(__name__)

weekly_schedule = {
'Monday': {'hour': '16'},
'Tuesday': {'hour': '15'},
'Wednesday': {'hour': '14'},
'Thursday': {'hour': '13'},
'Friday': {'hour': '12'},
}

scheduler=BackgroundScheduler()

def schedule_turn_ons(schedule):
    for day, schedtime in schedule.items():
        scheduler.add_job(func=TurnOn, trigger='cron', day_of_week=day, hour=schedtime['hour'], id=f'turn_on_job{day}')
        scheduler.add_job(func=TurnOff, trigger='cron', day_of_week=day, hour='24', id=f'turn_off_job{day}')


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
    <p>Advanced Flash</p>
    <br>
    <form method="get" action="/flash">
    <label for="flashes">Flashes</label>
    <input type="number" id="flashes" name="flashes" min="1" max="100">
    <label for="interval">Flash Interval</label>
    <input type="number" id="time_interval" name="time_interval" min=".001" max="10" step="any">
    <input type="submit" value="Submit">
    </form>

    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    schedule_turn_ons(weekly_schedule)
    scheduler.start()
