from RPi import GPIO
from time import sleep
import sys
import math

clk = 31
dt = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)
time = 0
lastTime = 0
timeDiff = 1
lastTimeDiff = 1
sleepConstant = 0.001

lineConstant = 10
lineTotal = 0
lineCurrent = 0
currentCounter = 0
muhammadConstant = 2.2

try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if (timeDiff == 0):
                timeDiff = lastTimeDiff
            #if (time == 0):
                #time = 1
            if dtState != clkState:
                #counter += 1 * abs(math.log(1/abs(time))/math.log(15))
                currentCounter += 1 * muhammadConstant ** (abs(1/time))
                counter += 1 * muhammadConstant ** (abs(1/time))
            else:
                 #counter -= 1 * abs(math.log(1/abs(time))/math.log(15))
                 currentCounter -= 1 * muhammadConstant ** (abs(1/time))
                 counter -= 1 * muhammadConstant ** (abs(1/time))
            if ((abs(currentCounter % lineConstant) >= lineConstant/2) and (currentCounter != 0)):
                lineCurrent += round(currentCounter / lineConstant)
                lineTotal += currentCounter
                currentCounter = 0
                print("LINES = " + str(lineCurrent))
            if (time != 50000):
                print(counter)
                #print("Time " + str(time))
                #print("Speed " + str(1 / time))
                #print("test " + str(counter / (timeDiff)))
                #print("Change in time: " + str(timeDiff))
                lastTimeDiff = timeDiff
                timeDiff = time-lastTime
                lastTime = time
            time = 0
        clkLastState = clkState
        sleep(sleepConstant)
        if (time < 300000 * sleepConstant):
            time += 1
finally:
    GPIO.cleanup()


