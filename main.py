import RPi.GPIO as GPIO
import time
import sys
import scheduler



GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

gatepin=11

GPIO.setup(gatepin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

def TurnOn():
    GPIO.output(gatepin, 1)

def TurnOff():
    GPIO.output(gatepin, 0)

def Flash(**kwargs):
    flashes=kwargs.get(flashes, default=10)
    time=kwargs.get(time, default=10)
    endState=kwargs.get(endState, default=0)
    for flash in range(flashes):
        TurnOn()
        time.sleep(time)
        TurnOff()
        time.sleep(time)
        if(flash == flashes-1) and endState:
            TurnOn()

sys.argv[1]()
