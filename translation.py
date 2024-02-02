# Raspberry Pi Code
import time
import gpiozero
import threading
import ast

open('demofile.txt','w').close() # Reset sample output
with open('UEBGrade2Lib', 'r') as f:
    data = f.read()
brailleLib = ast.literal_eval(data)

spaceBar = gpiozero.DigitalInputDevice(f"BOARD23", pull_up = True)

hallEffect = []
for pin in [40, 38, 26, 24, 21 ,22]:
    hallEffect.append(gpio.zero.DigitalInputDevice(f"BOARD{pin}", pull_up = True))
    
currentBinary = '000000'
spaceBarPressed = 0

def hallEffectRefresh():
    f = open("demofile.txt", "a")
    global hallEffect
    global currentBinary
    global spaceBarPressed
    if spaceBar.value:
        spaceBarPressed = 1
        i = 0
        for sensor in hallEffect:
            if sensor.value:
                currentBinary = currentBinary[:i] + '1' + currentBinary[i + 1:]
            i+=1
    elif spaceBarPressed:
        spaceBarPressed = 0
        print(brailleLib[currentBinary], end = '', flush = True)
        f.write(brailleLib[currentBinary])
        currentBinary = '000000'
        
    f.close()
    threading.Timer(.1, hallEffectRefresh).start()
    
print("\n============================")
print("LEAP Hall Effect Testing Tool")
print("\n============================\n")
