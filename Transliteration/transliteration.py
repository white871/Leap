import time
import gpiozero
import subprocess
from multiprocessing import Process
from transliterateBinary import transliterateBin
from GUITest import gui

open('output.txt', 'w').close()
spaceBar = gpiozero.DigitalInputDevice(f"BOARD23", pull_up = True)
hallEffect = []
for pin in [26, 38, 40, 24, 21, 22]:
    hallEffect.append(gpiozero.DigitalInputDevice(f"BOARD{pin}", pull_up = True))
outArray = []
for x in range(20):
    outArray.append("")
    
binArray = []
for x in range(20):
    binArray.append("")

currentBinary = '000000'
spaceBarPressed = 0
currentLine = 0

f_bin = open("tempBin.txt", "w")
f_bin.close()

f_out = open("transliterateOutput.txt", "w")
f_out.close()


print("Begin Transliteration.")

def hallEffectRefresh():
    global hallEffect
    global currentBinary
    global spaceBarPressed
    global currentLine
    global f_bin
    global binArray
    
    while(True):
        if (spaceBar.value):
            spaceBarPressed = 1
            i = 0
            for sensor in hallEffect:
                if (sensor.value):
                    currentBinary = currentBinary[:i] + '1' + currentBinary[i + 1:]
                i += 1
        elif (spaceBarPressed):
            spaceBarPressed = 0
            f = open("currentLine.txt", "r")
            currentLine = int(f.read())
            f.close()
            binArray[currentLine] += currentBinary
            currentBinary = '000000'
            f_bin = open("tempBin.txt", "w")
            for line in binArray:
                f_bin.write(line + "\n")
            f_bin.close()
            
        time.sleep(0.1)
        

    
def transliterate():
    while(True):  
        f_bin = open("tempBin.txt", "r")
        f_out = open("transliterateOutput.txt", "w")
        for line in f_bin.readlines():
            f_out.write(transliterateBin(line) + "\n")
        f_out.close()

        time.sleep(0.5)

def encodeRotation():
    subprocess.call("python encoderv4.py", shell = True)

p1 = Process(target = hallEffectRefresh)
p1.start()
p2 = Process(target = transliterate)
p2.start()
p3 = Process(target = encodeRotation)
p3.start()

gui("transliterateOutput.txt")


