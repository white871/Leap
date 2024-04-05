import time
import gpiozero
import threading

brailleLib = {
        "001000" : "a",
        "010000" : ",",
        "011000" : "b",
        "100000" : "'",
        "101000" : "k",
        "110000" : ";",
        "111000" : "l",


        "000100" : "\4/",
        "001100" : "c",
        "010100" : "i",
        "011100" : "f",
        "100100" : "\34/",
        "101100" : "m",
        "110100" : "s",
        "111100" : "p",


        "000010" : "\5/",
        "001010" : "e",
        "010010" : ":",
        "011010" : "h",
        "100010" : "\35/",
        "101010" : "o",
        "110010" : "!",
        "111010" : "r",


        "000110" : "\45/",
        "001110" : "d",
        "010110" : "j",
        "011110" : "g",
        "100110" : "\345/",
        "101110" : "n",
        "110110" : "t",
        "111110" : "q",
        
        "000001" : "undefined",
        "001001" : "\16/",
        "010001" : "\26/",
        "011001" : "undefined",
        "100001" : "-",
        "101001" : "u",
        "110001" : "”",
        "111001" : "v",


        "000101" : "\46/",
        "001101" : "undefined",
        "010101" : "\246/",
        "011101" : "¤",
        "100101" : "undefined",
        "101101" : "x",
        "110101" : "∫",
        "111101" : "\12346/",


        "000011" : "\156/",
        "001011" : ".",
        "010011" : "\1256/",
        "011011" : "”",
        "100011" : "z",
        "101011" : "’",
        "110011" : "undefined",
        "111011" : "undefined",


        "000111" : "\456/",
        "100111" : "\1456/",
        "010111" : "w",
        "110111" : "12456",
        "001111" : "y",
        "101111" : "undefined",
        "011111" : "\123456/",
        "111111" : "undefined",
        
        "000000" : " "
}
open('demofile.txt', 'w').close()
spaceBar = gpiozero.DigitalInputDevice(f"BOARD23", pull_up = True)
hallEffect = []
for pin in [40, 38, 26, 24, 21, 22]:
    hallEffect.append(gpiozero.DigitalInputDevice(f"BOARD{pin}", pull_up = True))
    
currentBinary = '000000'
spaceBarPressed = 0

def hallEffectRefresh():
    f = open("demofile.txt", "a")
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
        print(brailleLib[currentBinary], end='', flush=True)
        f.write(brailleLib[currentBinary])
        currentBinary = '000000'
    
    f.close()
    threading.Timer(.1, hallEffectRefresh).start()

print("\n=============================")
print("LEAP Hall Effect Testing Tool")
print("=============================\n")
hallEffectRefresh()
