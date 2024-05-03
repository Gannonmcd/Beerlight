import RPi.GPIO as GPIO
import time
import sys
#import scheduler



GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

gatepin=11

GPIO.setup(gatepin, GPIO.OUT)

def TurnOn():
    GPIO.output(gatepin, 1)
    print('turned on')

def TurnOff():
    GPIO.output(gatepin, 0)

def Flash(**kwargs):
    flashes=kwargs.get('flashes', 10)
    time_interval=kwargs.get('time_interval', .25)
    endState=kwargs.get('endState', 1)
    for flash in range(flashes):
        TurnOn()
        time.sleep(time_interval)
        TurnOff()
        time.sleep(time_interval)
        if(flash == flashes-1) and endState:
            TurnOn()

if sys.argv[1]=='1': TurnOn()
if sys.argv[1]=='2': TurnOff()
if sys.argv[1]=='3': Flash()
print('done')
