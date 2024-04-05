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
timeCap = 20000000
slimeCapstant = timeCap * sleepConstant

lineConstant = 12
lineTotal = 0
lineCurrent = 0
lineChanged = True
currentCounter = 0
muhammadConstant = 1.1
micahCount = 0

try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState: # checks if knob is moving
            if (timeDiff == 0):
                timeDiff = lastTimeDiff
                
            if (time > 1): # checks if the knob is not scrolling at "max speed"
                if (lastTime == 1): # resets the count    if the user slowed down from max speed
                    micahCount = 0
                else:
                    micahCount += 1 # increases the count to check how long it took to hit max speed
            if (wee == True and time == slimeCapstant): # resets the count if the user isnt scrolling
                micahCount = 0
            muhammadEquation = 1 + muhammadConstant ** (-(.15 * micahCount))
            #if (time == 0):
                #time = 1
            if dtState != clkState: # checks if the knob is scrolling counter clockwise
                #counter += 1 * abs(math.log(1/abs(time))/math.log(15))
                currentCounter += muhammadEquation ** (time == 1)#muhammadConstant ** (abs(1/time))
                lineChange = currentCounter
                counter += muhammadEquation ** (time == 1)#1 * muhammadConstant ** (abs(1/time))
            else: # Activates if the knob is scrolling clockwise
                 #counter -= 1 * abs(math.log(1/abs(time))/math.log(15))
                 currentCounter -= muhammadEquation ** (time == 1)#1 * muhammadConstant ** (abs(1/time))
                 lineChange = currentCounter
                 counter -= muhammadEquation ** (time == 1)#1 * muhammadConstant ** (abs(1/time))
            
            if lineChange > lineConstant: # moves down a line once it passes the threshold
                lineCurrent = round(counter / lineConstant)
                lineChange = 0
                currentCounter = 0
                print("LINES = " + str(lineCurrent))
                lineChanged = True
            if lineChange < (-1 * lineConstant): # moves up a line once it passes the threshold
                lineCurrent = round(counter / lineConstant)
                lineChange = 0
                currentCounter = 0
                print("LINES = " + str(lineCurrent))
                lineChanged = True
            if counter < 0:
                counter = 0
                lineCurrent = 0 
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
        clkLastState = clkState # updates the "previous position"
        #sleep(sleepConstant) # time between iterations
        if (time < slimeCapstant): # checks if scroll knob has been stagnant for a set time
            time += 1
            wee = True
        elif (time == slimeCapstant and wee): # notifies us once if scroll knob has been stagnant
            print("TIME DONE MUHAMMAD WEEEEE")
            wee = False
            if (time == slimeCapstant and currentCounter < -lineConstant * 3 / 5): # if knob is stagnant, jumps to the nearest line
                print("muhammad pee?>")
                if currentCounter < 0:
                    lineCurrent -= 1
                    print("LINES = " + str(lineCurrent))
                    lineChanged = True
                currentCounter = 0
            if (time == slimeCapstant and currentCounter > lineConstant * 3 / 5): # if knob is stagnant, jumps to the nearest line
                print("muhammad pee?>")
                if currentCounter > 0:
                    lineCurrent += 1
                    print("LINES = " + str(lineCurrent))
                    lineChanged = True
                currentCounter = 0
        if lineChanged:    
            f_out = open("currentLine.txt", "w")
            f_out.write(str(lineCurrent))
            f_out.close()
            lineChanged = False
finally:
    GPIO.cleanup()


