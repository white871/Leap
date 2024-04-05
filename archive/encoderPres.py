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

lineConstant = 20
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
            if dtState != clkState:
                currentCounter += 1 * muhammadConstant ** (abs(1/time))
                lineChange = currentCounter
                counter += 1 * muhammadConstant ** (abs(1/time))
            else:
                 currentCounter -= 1 * muhammadConstant ** (abs(1/time))
                 lineChange = currentCounter
                 counter -= 1 * muhammadConstant ** (abs(1/time))
            if (time == 1000 and currentCounter < lineConstant / 4):
                if currentCounter < 0:
                    lineCurrent -= 1
                currentCounter = 0
            if (time == 1000 and currentCounter > lineConstant * 3 / 4):
                if currentCounter > 0:
                    lineCurrent += 1
                    print("LINES = " + str(lineCurrent))
                currentCounter = 0
            if lineChange > lineConstant:
                lineCurrent = round(counter / lineConstant)
                lineChange = 0
                currentCounter = 0
                print("LINES = " + str(lineCurrent))
            if lineChange < (-1 * lineConstant):
                lineCurrent = round(counter / lineConstant)
                lineChange = 0
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
        if (time < 1000000 * sleepConstant):
            time += 1
            wee = True
        #elif (time == 1000000 * sleepConstant and wee):
            #print("TIME DONE MUHAMMAD WEEEEE")
            #wee = False
finally:
    GPIO.cleanup()


