import ast
import csv
import json

with open('brailleLib.txt', 'r') as f:
    data = f.read()
brailleLib = ast.literal_eval(data)

with open('brailletobinary.txt', 'r', encoding = "utf-8") as f:
    data = f.read()
b2b = ast.literal_eval(data)

#a blind but accelerate before pound
input = "⠠⠮⠀⠋⠌⠀⠹⠬⠀⠠⠊⠀⠓⠑⠜⠙⠀⠴⠀⠠⠠⠠⠃⠁⠝⠛⠀⠏⠪⠀⠏⠕⠏⠠⠄⠀⠯⠀⠠⠊⠀⠴⠀⠇⠀⠠⠠⠱⠁⠞⠀⠊⠀⠴⠀⠎⠀⠎⠉⠜⠫⠀⠠⠯⠀⠠⠊⠀⠗⠁⠝⠀⠇⠀⠁⠀⠙⠕⠶⠽⠀⠔⠞⠕⠀⠮⠀⠁⠇⠇⠑⠽⠀⠠⠠⠃⠕⠕⠍⠀⠁⠝⠕⠮⠗⠀⠐⠕⠀⠠⠠⠃⠁⠍⠀⠁⠝⠕⠮⠗⠀⠐⠕⠀⠠⠯⠀⠮⠝⠀⠭⠀⠴⠀⠕⠧⠻⠀⠠⠠⠮⠀⠠⠠⠢⠙"

inputB = ""

for char in input:
    inputB += b2b[char]

inputarr = []
i = 0

while (i <= len(inputB) - 6):
    newStr = ""

    for j in range(6):
        newStr += inputB[i + j]
    inputarr.append(newStr)
    i += 6

i = 0
translatedOutput = ""
inputarr.insert(0, "000000")
inputarr.append("000000")
while (i < len(inputarr)):
    fiveLong = ""
    fourLong = ""
    threeLong = ""
    twoLong = ""
    oneLong = ""
    if i < len(inputarr) - 4:
        fiveLong = inputarr[i] + inputarr[i + 1] + inputarr[i + 2] + inputarr[i + 3] + inputarr[i + 4]
    if i < len(inputarr) - 3:
        fourLong = inputarr[i] + inputarr[i + 1] + inputarr[i + 2] + inputarr[i + 3]
    if i < len(inputarr) - 2:
        threeLong = inputarr[i] + inputarr[i + 1] + inputarr[i + 2]
    if i < len(inputarr) - 1:
        twoLong = inputarr[i] + inputarr[i + 1]
    oneLong = inputarr[i]
    translated = False
    if fiveLong in brailleLib.keys():
        for possibleOut in brailleLib[fiveLong]:
            if "./" in possibleOut:
                translatedOutput += possibleOut.replace("^", "")
                i += 5
                translated = True
            if "_" in possibleOut:
                if i > 0 and i < len(inputarr) - 1:
                    if (inputarr[i - 1] == "000000" or "./" in brailleLib[inputarr[i - 1]][0]) and inputarr[i + 5] == "000000":
                        translatedOutput += possibleOut.replace("_", "")
                        i += 5
                        translated = True
            if possibleOut.startswith('^') and possibleOut.endswith('^') and not translated:
                if i > 0 and i < len(inputarr) - 1:
                    if inputarr[i - 1] != "000000" and inputarr[i + 5] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 5
                        translated = True
                    else:
                        continue
            if possibleOut.startswith('^') and not translated:
                if i > 0:
                    if inputarr[i - 1] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 5
                        translated = True
            if possibleOut.endswith('^') and not translated:
                if i < len(inputarr) - 1:
                    if inputarr[i + 5] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 5
                        translated = True
        if not translated:
            if fourLong not in brailleLib.keys() and threeLong not in brailleLib.keys() and twoLong not in brailleLib.keys() and oneLong not in brailleLib.keys():  
                translatedOutput += brailleLib[fiveLong][0]
                i += 5
                translated = True
    if fourLong in brailleLib.keys() and not translated:
        for possibleOut in brailleLib[fourLong]:
            if "./" in possibleOut:
                translatedOutput += possibleOut.replace("^", "")
                i += 4
                translated = True
            if "_" in possibleOut:
                if i > 0 and i < len(inputarr) - 1:
                    if (inputarr[i - 1] == "000000" or "./" in brailleLib[inputarr[i - 1]][0]) and inputarr[i + 4] == "000000":
                        translatedOutput += possibleOut.replace("_", "")
                        i += 4
                        translated = True
            if possibleOut.startswith('^') and possibleOut.endswith('^') and not translated:
                if i > 0 and i < len(inputarr) - 1:
                    if inputarr[i - 1] != "000000" and inputarr[i + 4] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 4
                        translated = True
                    else:
                        continue
            if possibleOut.startswith('^') and not translated:
                if i > 0:
                    if inputarr[i - 1] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 4
                        translated = True
            if possibleOut.endswith('^') and not translated:
                if i < len(inputarr) - 1:
                    if inputarr[i + 4] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 4
                        translated = True
        if not translated:
            if threeLong not in brailleLib.keys() and twoLong not in brailleLib.keys() and oneLong not in brailleLib.keys():  
                translatedOutput += brailleLib[fourLong][0]
                i += 4
                translated = True
    if threeLong in brailleLib.keys() and not translated:
        for possibleOut in brailleLib[threeLong]:
            if "./" in possibleOut:
                translatedOutput += possibleOut.replace("^", "")
                i += 3
                translated = True
            if "_" in possibleOut:
                if i > 0 and i < len(inputarr) - 1:
                    if (inputarr[i - 1] == "000000" or "./" in brailleLib[inputarr[i - 1]][0]) and inputarr[i + 3] == "000000":
                        translatedOutput += possibleOut.replace("_", "")
                        i += 3
                        translated = True
            if possibleOut.startswith('^') and possibleOut.endswith('^') and not translated:
                if i > 0 and i < len(inputarr) - 1:
                    if inputarr[i - 1] != "000000" and inputarr[i + 3] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 3
                        translated = True
                    else:
                        continue
            if possibleOut.startswith('^') and not translated:
                if i > 0:
                    if inputarr[i - 1] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 3
                        translated = True
            if possibleOut.endswith('^') and not translated:
                if i < len(inputarr) - 1:
                    if inputarr[i + 3] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 3
                        translated = True
        if not translated:
            if twoLong not in brailleLib.keys() and oneLong not in brailleLib.keys():  
                translatedOutput += brailleLib[threeLong][0]
                i += 3
                translated = True
    if twoLong in brailleLib.keys() and not translated:
        for possibleOut in brailleLib[twoLong]:
            if "./" in possibleOut:
                translatedOutput += possibleOut.replace("^", "")
                i += 2
                translated = True
            if "_" in possibleOut:
                if i > 0 and i < len(inputarr) - 2:
                    if (inputarr[i - 1] == "000000" or "./" in brailleLib[inputarr[i - 1]][0]) and inputarr[i + 2] == "000000":
                        translatedOutput += possibleOut.replace("_", "")
                        i += 2
                        translated = True
            if possibleOut.startswith('^') and possibleOut.endswith('^') and not translated:
                if i > 0 and i < len(inputarr) - 1:
                    if inputarr[i - 1] != "000000" and inputarr[i + 2] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 2
                        translated = True
                    else:
                        continue
            if possibleOut.startswith('^') and not translated:
                if i > 0:
                    if inputarr[i - 1] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 2
                        translated = True
            if possibleOut.endswith('^') and not translated:
                if i < len(inputarr) - 1:
                    if inputarr[i + 2] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 2
                        translated = True
        if not translated:
            if oneLong not in brailleLib.keys():  
                translatedOutput += brailleLib[twoLong][0]
                i += 2
                translated = True
    if oneLong in brailleLib.keys() and not translated:
        for possibleOut in brailleLib[oneLong]:
            if "./" in possibleOut:
                translatedOutput += possibleOut.replace("^", "")
                i += 1
                translated = True
            if "_" in possibleOut:
                if i > 0 and i < len(inputarr) - 1:
                    if (inputarr[i - 1] == "000000" or "./" in brailleLib[inputarr[i - 1]][0]) and inputarr[i + 1] == "000000":
                        translatedOutput += possibleOut.replace("_", "")
                        i += 1
                        translated = True
            if possibleOut.startswith('^') and possibleOut.endswith('^') and not translated:
                if i > 0 and i < len(inputarr) - 1:
                    if inputarr[i - 1] != "000000" and inputarr[i + 1] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 1
                        translated = True
                    else:
                        continue
            if possibleOut.startswith('^') and not translated:
                if i > 0:
                    if inputarr[i - 1] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 1
                        translated = True
            if possibleOut.endswith('^') and not translated:
                if i < len(inputarr) - 1:
                    if inputarr[i + 1] != "000000":
                        translatedOutput += possibleOut.replace("^", "")
                        i += 1
                        translated = True
        if not translated:
            translatedOutput += brailleLib[oneLong][0]
            i += 1
            translated = True
    if not translated:
        i += 1

translatedOutput = translatedOutput.replace("_", "")

while("./" in translatedOutput):
    if "./capital letter" in translatedOutput:
        capitalLetter_i = translatedOutput.find("./capital letter") + 16
        translatedOutput = translatedOutput[:capitalLetter_i] + translatedOutput[capitalLetter_i].upper() + translatedOutput[capitalLetter_i + 1:]
        translatedOutput = translatedOutput.replace("./capital letter", "", 1)
    if "./capital word" in translatedOutput:
        capitalWord_start = translatedOutput.find("./capital word") + 14
        capitalWord_end = translatedOutput[capitalWord_start:].find(" ") + capitalWord_start
        translatedOutput = translatedOutput[:capitalWord_start] + translatedOutput[capitalWord_start:capitalWord_end].upper() + translatedOutput[capitalWord_end:]
        translatedOutput = translatedOutput.replace("./capital word", "", 1)
    if "./capital passage" in translatedOutput:
        capitalPassage_start = translatedOutput.find("./capital passage") + 17
        capitalPassage_end = translatedOutput[capitalPassage_start:].find("./capital terminator") + capitalPassage_start
        translatedOutput = translatedOutput[:capitalPassage_start] + translatedOutput[capitalPassage_start:capitalPassage_end].upper() + translatedOutput[capitalPassage_end:]
        translatedOutput = translatedOutput.replace("./capital passage", "", 1)
        translatedOutput = translatedOutput.replace("./capital terminator", "", 1)

translatedOutput = translatedOutput.strip()
print(translatedOutput)

