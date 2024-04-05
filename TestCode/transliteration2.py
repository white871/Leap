import ast
import csv
import json
import math
def BRtoBI(braille, brailletobinary):
    binInput = ''
    for char in braille:
        binInput += brailletobinary[char]
    return binInput

def searchBinary(brailleLib, binInput):
    possible = []
    binlist = []
    length = 5
    i = 0
    possible = []
    while i < len(binInput):
        length = 5 if len(binInput) >= 30 else binInput
        while length > 0:
            if binInput[i:i + length * 6] in brailleLib.keys():
                convert = brailleLib[binInput[i:i+length*6]]
                binlist.append(binInput[i:i+length*6])
                
                possible.append(convert)
                break
            length-=1
        i+=6 * length
    return possible, binlist

def checkKey(possible, ind, j, checkB, checkE):
    key = False
    mtch = False
    print(checkB)
    print(checkE)
    print(ind)
    if checkB == '_' and checkE == '_':
        key = True
        if ind == len(possible) - 1:
            mtch = possible[ind - 1] == ' '
        elif ind == 0:
            mtch = possible[ind + 1] == ' '
        else:
            mtch = possible[ind + 1] == [' '] and possible[ind - 1] == [' ']
    elif checkB == '^' or checkE == '^':
        key = True
        if checkE == '^' and checkB == '^':
            mtch = possible[ind - 1] != [' '] and possible[ind + 1] != [' '] and ind > 0 and ind < len(possible) - 1
        if checkB == '^':
            mtch = possible[ind - 1] != [' '] and ind > 0
        if checkE == '^':
            mtch = possible[ind + 1] != [' '] and ind < len(possible) - 1
    return key, mtch

def evaluatePossible(possible, binlist):
    i = 0
    translit = ""
    for i in range(len(possible)):
        j = 0
        fnd = False
        while(j < len(possible[i])):
            key, fnd = checkKey(possible, i, j, possible[i][j][0], possible[i][j][-1])
            if (key and fnd) or (not(key) and not(fnd)):
                translit = translit + possible[i][j].replace('_', '').replace('^', '')
                break   
            j+=1
            
        if j == len(possible[i]) and not(fnd): # No extra character found or at end of list
            translit = translit + possible[i][0]
            binlist, possible = noneFound(possible, i, binlist)
            #i-=1

            
    return translit

def noneFound(possible, inv, binlist):
    print(binlist[inv:-1])
    
    length = len(binlist[inv]) / 6
    #binChange = binlist[inv]
    #binlist[inv] = binChange[0: (length - 1)]
    #binlist[inv] = binChange[length / 2]
    return binlist, possible

# Translate Braille to Binary Code (if applicable )
with open('brailletobinary.txt', 'r') as f:
    data = f.read()
b2b = ast.literal_eval(data)
brInput = "⠋⠥⠝⠙⠁⠰⠞⠁⠇"
binInput = BRtoBI(brInput, b2b)

# Open Braille Library
with open('brailleLib.txt', 'r') as f:
    data = f.read()
brailleLib = ast.literal_eval(data)
possible, binlist = searchBinary(brailleLib, binInput)
print(possible)
print(binlist)
translit = evaluatePossible(possible, binlist)
print(translit)