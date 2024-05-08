from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
breakflag=False
sosmode=False

logger=logging.getLogger(__name__)

weekly_schedule = {
'mon': {'hour': '16'},
'tue': {'hour': '15'},
'wed': {'hour': '14'},
'thu': {'hour': '13'},
'fri': {'hour': '12'},
}

scheduler=BackgroundScheduler()

def schedule_turn_ons(schedule):
    for day, schedtime in schedule.items():
        scheduler.add_job(func=TurnOn, trigger='cron', day_of_week=day, hour=schedtime['hour'], id=f'turn_on_job{day}')
        scheduler.add_job(func=TurnOff, trigger='cron', day_of_week=day, hour='23', id=f'turn_off_job{day}')


app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
gatepin = 11
GPIO.setup(gatepin, GPIO.OUT)

def TurnOn():
    GPIO.output(gatepin, 1)
    global breakflag
    breakflag=True
    return "Cheers!"

def TurnOff():
    GPIO.output(gatepin, 0)
    global breakflag
    breakflag=True
    return "Turned Off"

def BreakSOS():
    global breakflag
    breakflag=True
    return "SOS Mode Deactivated"

def Flash(flashes=10, time_interval=0.25, endState=1):
    for flash in range(flashes):
        GPIO.output(gatepin, 1)
        time.sleep(time_interval)
        GPIO.output(gatepin, 0)
        time.sleep(time_interval)
        if (flash == flashes - 1) and endState:
            GPIO.output(gatepin, 1)
    return f"Flashed {flashes} times"

def SOS():
    global sosmode
    sosmode=True
    while True:
        Flash(3, .25, endState=0)
        time.sleep(.25)
        Flash(3, .75, endState=0)
        time.sleep(.25)
        Flash(3, .25, endState=0)
        time.sleep(.25)
        global breakflag
        if breakflag==True:
            breakflag=False
            break

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

@app.route('/sos', methods=['GET'])
def sos():
    return SOS()

@app.route('/break', methods=['GET'])
def breakSOS():
    return BreakSOS()

@app.route('/')
def index():
    global sosmode
    if sosmode:
        return '''
        <h1>SOS Mode Active</h1>
        <br>
        <a href="/break">Cancel SOS Mode</a>
        '''
    else:
        return '''
        <h1>Beer Light Control</h1>
        <p><a href="/on">Turn On</a></p>
        <p><a href="/off">Turn Off</a></p>
        <p><a href="/flash">Flash</a></p>
        <p><a href="/sos">SOS</a></p>
        <h2>Advanced Flash</h2>
        <form method="get" action="/flash">
        <label for="flashes">Flashes</label>
        <input type="number" id="flashes" name="flashes" min="1" max="100">
        <label for="interval">Flash Interval</label>
        <input type="number" id="time_interval" name="time_interval" min=".001" max="10" step="any">
        Light Endstate
        <input type="radio" id="endStateOn" name="endState" Value="1">
        <label for="On">On</label>
        <input type="radio" id="endStateOff" name="endState" Value="0">
        <label for="Off">Off</label><br>
        <input type="submit" value="Submit">
        </form>
        '''



if __name__ == '__main__':
    schedule_turn_ons(weekly_schedule)
    scheduler.start()
    scheduler.print_jobs()
    try:
        app.run(debug=True, host='0.0.0.0', port=80)
    finally:
        scheduler.shutdown()

