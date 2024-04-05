import time
import gpiozero
import threading
from transliterateBinary import transliterateBin

open('output.txt', 'w').close()
spaceBar = gpiozero.DigitalInputDevice(f"BOARD23", pull_up = True)
hallEffect = []
for pin in [26, 38, 40, 24, 21, 22]:
    hallEffect.append(gpiozero.DigitalInputDevice(f"BOARD{pin}", pull_up = True))
    
currentBinary = '000000'
spaceBarPressed = 0

f_reset = open("outputBin.txt", "w")
f_reset.close()

print("Begin Transliteration.")

def hallEffectRefresh():
    f = open("outputBin.txt", "a")
    global hallEffect
    global currentBinary
    global spaceBarPressed
    if (spaceBar.value):
        spaceBarPressed = 1
        i = 0
        for sensor in hallEffect:
            if (sensor.value):
                currentBinary = currentBinary[:i] + '1' + currentBinary[i + 1:]
            i += 1
    elif (spaceBarPressed):
        spaceBarPressed = 0
        f.write(currentBinary)
        currentBinary = '000000'
    
    f.close()
    threading.Timer(.1, hallEffectRefresh).start()
    
def transliterate():
    f = open("outputBin.txt", "r")
    
    inputB = f.read()
    f.close()
    transliterateBin(inputB)
    threading.Timer(.5, transliterate).start()

hallEffectRefresh()
transliterate()
