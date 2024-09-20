import ast
import csv
import json

with open('brailleLib.txt', 'r') as f:
    data = f.read()
brailleLib = ast.literal_eval(data)

with open('brailletobinary.txt', 'r', encoding = "utf-8") as f:
    data = f.read()
b2b = ast.literal_eval(data)

def transliterateBin(inputB):
    global brailleLib
    global b2b
    global translated
    global translatedOutput
    global i
    global lastOutput
    
    
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
    lastOutput = ""
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

        def findOutput(whatLong, howLong):
            global translated
            global translatedOutput
            global i
            global lastOutput
            if whatLong in brailleLib.keys():
                for possibleOut in brailleLib[whatLong]:
                    if "./" in possibleOut:
                        translatedOutput += possibleOut.replace("^", "")
                        lastOutput = possibleOut.replace("^", "")
                        i += howLong
                        translated = True
                    if "_" in possibleOut:
                        if i > 0 and i < len(inputarr) - 1:
                            expand = False
                            if (inputarr[i - 1] == "000000") and (inputarr[i + howLong] == "000000"):
                                expand = True
                            if (inputarr[i + howLong] in brailleLib.keys()):
                                if (inputarr[i - 1] == "000000" or "./" in lastOutput) and (not brailleLib[inputarr[i + howLong]][0].replace("^", "").replace("_", "").isalnum()):
                                    expand = True
                            if (expand):
                                translatedOutput += possibleOut.replace("_", "")
                                lastOutput = possibleOut.replace("_", "")
                                i += howLong
                                translated = True
                    if possibleOut.startswith('^') and possibleOut.endswith('^') and not translated:
                        if i > 0 and i < len(inputarr) - 1:
                            if inputarr[i - 1] != "000000" and inputarr[i + howLong] != "000000" and not "./" in lastOutput:
                                translatedOutput += possibleOut.replace("^", "")
                                lastOutput = possibleOut.replace("^", "")
                                i += howLong
                                translated = True
                            else:
                                continue
                    if possibleOut.startswith('^') and not translated:
                        if i > 0:
                            if inputarr[i - 1] != "000000":
                                translatedOutput += possibleOut.replace("^", "")
                                lastOutput = possibleOut.replace("^", "")
                                i += howLong
                                translated = True
                    if possibleOut.endswith('^') and not translated:
                        if i < len(inputarr) - 1:
                            if inputarr[i + howLong] != "000000":
                                translatedOutput += possibleOut.replace("^", "")
                                lastOutput = possibleOut.replace("^", "")
                                i += howLong
                                translated = True
                if not translated and howLong == 5:
                    if fourLong not in brailleLib.keys() and threeLong not in brailleLib.keys() and twoLong not in brailleLib.keys() and oneLong not in brailleLib.keys():  
                        translatedOutput += brailleLib[whatLong][0]
                        lastOutput = brailleLib[whatLong][0]
                        i += howLong
                        translated = True
                if not translated and howLong == 4:
                    if threeLong not in brailleLib.keys() and twoLong not in brailleLib.keys() and oneLong not in brailleLib.keys():  
                        translatedOutput += brailleLib[whatLong][0]
                        lastOutput = brailleLib[whatLong][0]
                        i += howLong
                        translated = True
                if not translated and howLong == 3:
                    if twoLong not in brailleLib.keys() and oneLong not in brailleLib.keys():  
                        translatedOutput += brailleLib[whatLong][0]
                        lastOutput = brailleLib[whatLong][0]
                        i += howLong
                        translated = True
                if not translated and howLong == 2:
                    if oneLong not in brailleLib.keys():  
                        translatedOutput += brailleLib[whatLong][0]
                        lastOutput = brailleLib[whatLong][0]
                        i += howLong
                        translated = True
                if not translated and howLong == 1:
                    if ("." in brailleLib[oneLong] or "," in brailleLib[oneLong] or "!" in brailleLib[oneLong]):
                        translatedOutput += brailleLib[oneLong][1]
                        lastOutput = brailleLib[oneLong][1]
                    else:
                        translatedOutput += brailleLib[oneLong][0]
                        lastOutput = brailleLib[oneLong][0]
                    i += 1
                    translated = True
        findOutput(fiveLong, 5)
        findOutput(fourLong, 4)
        findOutput(threeLong, 3)
        findOutput(twoLong, 2)
        findOutput(oneLong, 1)
        if not translated:
            i += 1

    translatedOutput = translatedOutput.replace("_", "")
    try:
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
            if "./numeric indicator" in  translatedOutput:
                a_to_n = {"a" : "1", "b" : "2", "c" : "3", "d" : "4", "e" : "5", "f" : "6", "g" : "7", "h" : "8", "i" : "9"}
                number_i = translatedOutput.find("./numeric indicator") + 19
                while (translatedOutput[number_i] in a_to_n.keys()):
                    translatedOutput = translatedOutput[:number_i] + a_to_n[translatedOutput[number_i]] + translatedOutput[number_i + 1:]
                    number_i += 1
                translatedOutput = translatedOutput.replace("./numeric indicator", "", 1)
        except:
            pass

    translatedOutput = translatedOutput.strip()
    f_out = open('transliterateOutput.txt', 'w')
    f_out.write(translatedOutput)
    f_out.close()
