import ast
import time
import pdb
with open('brailleLib.txt', 'r') as bL: 
    bLdata = bL.read()
bLib = ast.literal_eval(bLdata)

with open('nemethLib.txt', 'r') as nL:
    nLdata = nL.read()
nLib = ast.literal_eval(nLdata)

nums = {
  "010000" : "1",
  "011000": "2",
  "010010": "3",
  "010011": "4",
  "010001": "5",
  "011010": "6",
  "011011": "7",
  "011001": "8",
  "001010": "9",
  "001011": "0",
}
punctuation = {
    "010011": "." ,
    "011001" : "?",
    "011010" : "!",
    "001011" : '"',
}
# FLAGS
# CAP: Capitalization (1 -> letter, 2 -> word, 3 -> passage)
# NME: Nemeth (1 -> Transliterate into Nemeth, 0 -> Transliterate into UEB)
# NUM: Numeric indicator 
# PUN: Punctuation indicator
# FRACT: Fraction indicator
# SPC: Space indicator
# CONT: Item is both a flag and a character (Ex: ¢)
# MIX: Mixed fraction indicator
# GD1: Grade 1 indicator (Only for UEB)
NEMFlags = {
    "001111" : "./NUMIND",       # Numeric indicator
    "000100011100" : "./NUM", # $
    "000100100100" : "./NUM", # Cent symbol
    "111011" : "./NUM",       # Opening Parenthesis
    "001101" : "./NUM",       # Plus
    "001001" : "./NUM",       # Minus
    "110011" : "./NUM",       # Vertical Bar
    "001110" : "./NUM",       # Radical Sign
    "001101001001" : "./NUM", # Plus-minus sign
    "001001001101" : "./NUM", # Minus-plus sign
    "000111" : "./PUN",   
    "000001" : "./CAP",
    "000011" : "./GD1",
    "100111" : "./FRA",
    "000111100111" : "./MIX",
    "000111100011" : "./NEM", # Closing nemeth indicator
    "000111100101" : "./OPENNEM",
    "000001001000" : "./SWI",
    "000110" : "./SUP",
    "000010" : "./BASE",
    "110001" : "./SEG",
    "010101010010010010101010" : "./LINE",
    "110101101010" : "./RAY",
    "110111" : "./TERM",
    "110001" : "./OVER",
    "100011" : "./BAR",
    "000100" : "./BRACK",
    "0001110001000" : "./BOLD",
    "000101" : "./BRACE",
    "001110" : "./RAD",
    "000001100111" : "./COMS",
    "000001001111" : "./COME"
}
UEBFlags = {
    "000011" : "./GD1",
    "000011001000" : "./GD1TERM",
    "000001" : "./CAP",
    "000001001000": "./CAPTERM",
    "000111100101" : "./NEM",
    "000111100011" : "./CLOSENEM"
}


def transliterateBin(inputB):
    global \
        CAP, LEN, TRAN, NME, LIB, NUM, PUN, FRACT, \
        SPC, CONT, MIX, GD1, SUP, PASTFRACT, SWI, PASTSUP, MUL, PARENTH, RAD, PASTRAD, TRAN, \
        bLib, nLib, tlOut, prev, i, iarr, temp, posLen, possible
    LIB = CAP = LEN = TRAN = NME = PARENTH = SUP = NUM = PUN = FRACT = SPC = MUL = CONT = MIX = GD1 = PASTFRACT = PASTSUP = SWI = RAD = PASTRAD = TRAN = 0
    global flags
    NME = 1
    tlOut = ""
    prev = ""
    temp = ""
    iarr = []
    
    i = 0
    iarr.append("000000")
    while (i <= len(inputB) - 6):
        newStr = ""
        
        for j in range(6):
            newStr += inputB[i + j]
        iarr.append(newStr)
        i += 6
    iarr.append("000000")
    iarr.append("000000")
    possible = []
    i = 1
    while(i < len(iarr) - 1):
        TRAN = 0
        possible = [None] * (len(iarr[i:]) if len(iarr) - i < 5  else 5)
        posLen = len(possible)
        for k in range(6, -1, -1):
            if k < posLen:
                possible[posLen - k - 1] = ("".join(iarr[i:i+k+1]))
        
        #print(f"POSSIBLE: {possible}")

        def chkFlags(item):
            
            global i, iarr, tlOut, PUN, CAP, NUM, FRACT, NME, CONT, MIX, GD1, SUP, SWI, MUL, RAD, PASTFRACT, PASTSUP, PASTRAD
            if item in nLib.keys():
                CONT = 1;
            else:
                CONT = 0;
            if not NME and item in UEBFlags.keys():
                
                CAP += 1 if UEBFlags[item] == "./CAP" else CAP
                
                GD1 += 1 if UEBFlags[item] == "./GD1" else GD1
                if UEBFlags[item] == "./NEM":
                    NME = 1
                    if (iarr[i+1] == '000000'):
                        i = i+1
                    return 1
                return (CAP or GD1)
            if NME and item in NEMFlags.keys():
                if (iarr[i-1] == "000000"):
                    CAP = 0
                    
                CAP += 1 if (NEMFlags[item] == "./CAP" and FRACT == 0) else CAP
                PASTFRACT = FRACT
                PASTSUP = SUP
                PASTRAD = RAD
                if NEMFlags[item] == "./RAD":
                    RAD = 1
                    tlOut += u"\N{SQUARE ROOT}"
                    tlOut += '('
                if NEMFlags[item] == "./TERM":
                    RAD = 0
                    MUL = 0
                    if prev != u"\N{QUESTIONED EQUAL TO}":
                        tlOut += ')'
                
                if NEMFlags[item] == "./FRA" or NEMFlags[item] == "./COMS" or NEMFlags[item] == "./MIX":
                    FRACT += 1
                    if NEMFlags[item] == "./MIX":
                        tlOut += u"\N{MIDDLE DOT}"
                    tlOut += '('
                if ((NEMFlags[item] == "./NUMIND" or NEMFlags[item] == "./COME") and FRACT != 0):
                    FRACT -= 1
                    tlOut += ')'

                NUM = 1 if ((NEMFlags[item] == "./NUM" or NEMFlags[item] == "./NUMIND"  or NEMFlags[item] == "./SUP" and FRACT == 0) or FRACT or RAD) else NUM
                PUN = 1 if NEMFlags[item] == "./PUN" else PUN
                MIX = 1 if NEMFlags[item] == "./MIX" else MIX
                MUL = 1 if NEMFlags[item] == "./BASE" and not SUP else MUL
                SUP = 1 if NEMFlags[item] == "./SUP" else SUP
                SUP = 0 if NEMFlags[item] == "./BASE" else SUP
                SWI = 1 if NEMFlags[item] == "./SWI" else SWI
                if NEMFlags[item] == "./NEM" or SWI:
                    NME = 0
                    if (iarr[i+1] == '000000'):
                        i = i+1
                    return 1
                return (item in NEMFlags.keys())
            return 0
            
            
        def UEB(item):
            global iarr, i, tlOut, TRAN, CAP, GD1, NME, SWI, NUM, prev, posLen, possible
            punct = [".", ",", "!"]
            out = ""
            if prev == "./CLOSENEM":
                GD1 = 1
            else:
                GD1 = 0
            if prev == "./CAPTERM":
                CAP = 0
            if item == "000000":
                NUM = 0
                if SWI:
                    SWI = 0
                    NME = 1
                if CAP == 2:
                    CAP = 0
                if GD1 == 2:
                    GD1 = 0
            howlong = (int)(len(item) / 6)
            if GD1:
                if howlong > 1:
                    return
            spaceBefore = (iarr[i - 1] == "000000")
            spaceAfter = (iarr[i + howlong] == "000000")
            for perhaps in bLib[item]:
                if not TRAN and not GD1:
                    if "_" in perhaps:
                        expand = False
                        if spaceBefore and spaceAfter:
                            expand = True
                        if iarr[i + howlong] in bLib.keys():
                            if (iarr[i - 1] == "000000" or "./" in prev):
                                if not bLib[iarr[i + howlong]][0].replace("^", "").replace("_", "").isalnum():
                                    expand = True
                                    
                                elif (len(bLib[iarr[i + howlong]]) != 1 and bLib[iarr[i + howlong]][1] in punct and iarr[i + howlong + 1] == "000000"):
                                    expand = True
                            
                        if expand:
                            out = perhaps.replace("_", "")
                            prev = perhaps.replace("_", "")
                            TRAN = 1
                    if perhaps[0] == ('^') and perhaps[-1] == '^' and not TRAN:
                        if i > 0 and i < len(iarr) - 2:
                            if iarr[i - 1] != "000000" and iarr[i + howlong] != "000000" and not "./" in prev:
                                out = perhaps.replace("^", "")
                                prev = perhaps.replace("^", "")
                                TRAN = 1
                            else:
                                continue
                    if perhaps[0] == ('^') and not TRAN:
                        if i > 0:
                            if iarr[i - 1] != "000000":
                                out = perhaps.replace("^", "")
                                prev = perhaps.replace("^", "")
                                TRAN = 1
                    if perhaps[-1] == ('^') and not TRAN:
                        if i < len(iarr) - 2:
                            if iarr[i + howlong] != "000000":
                                out = perhaps.replace("^", "")
                                prev = perhaps.replace('^', "")
                                TRAN = 1
            if not TRAN and howlong == 5:
                if possible[1] not in bLib.keys() and possible[2] not in bLib.keys() and possible[3] not in bLib.keys() and possible[4] not in bLib.keys():
                    out = bLib[item][0]
                    prev = bLib[item][0]
                    TRAN = 1
            stPoint = posLen - howlong
            if not TRAN and howlong == 4:
                if possible[stPoint + 1] not in bLib.keys() and possible[stPoint + 2] not in bLib.keys() and possible[stPoint + 3] not in bLib.keys():
                    out = bLib[item][0]
                    prev = bLib[item][0]
                    TRAN = 1
            if not TRAN and howlong == 3:
                if possible[stPoint + 1] not in bLib.keys() and possible[stPoint + 2] not in bLib.keys():
                    out = bLib[item][0]
                    prev = bLib[item][0]
                    TRAN = 1
            if not TRAN and howlong == 2:
                if possible[stPoint + 1] not in bLib.keys():
                    out = bLib[item][0]
                    prev = bLib[item][0]
                    TRAN = 1
            if not TRAN and howlong == 1:
                if ("." in bLib[item] or "," in bLib[item] or "!" in bLib[item]):
                    out = bLib[item][1]
                    prev = bLib[item][1]
                else:
                    out = bLib[item][0]
                    prev = bLib[item][0]
                TRAN = 1
            if TRAN:
                match CAP: 
                    case 1:
                        out = out.capitalize()
                        CAP = 0
                    case 2: 
                        out = out.upper()
                    case 3:
                        out.upper()
                if NUM:
                    a_to_n = {"a" : "1", "b" : "2", "c" : "3", "d" : "4", "e" : "5", "f" : "6", "g" : "7", "h" : "8", "i" : "9"}
                    out = a_to_n[out]
                #print(out)
                out = out.replace("_", "").replace("^","")
                tlOut += out
                i += (int)(len(item) / 6)

        def NEM(item):
            global tlOut, i, iarr, TRAN, NUM, CAP, SPC, PUN, SUP, MUL, PASTFRACT, FRACT, PASTRAD, prev, temp, PARENTH
           
            if item == "000000" or item == "000001000000":
                if not PARENTH:
                    NUM = 0
                CAP = 0
                if SUP:
                    tlOut += ")"
                SUP = 0
                PUN = 0
            TRAN = 1
            
            if prev == "./BASE" and PASTSUP:
                tlOut += ")"
                    
            if prev == "./LINE":
                tlOut += r'$\overline{temp}$'
                temp = ""
                MUL = 0
            if PUN and item in punctuation.keys():
                out = punctuation[item]
            elif NUM and item in nums.keys(): 

                out = nums[item]
            else:
                out = nLib[item]
            #print(out)
            # Parentheses, Brackets, & Braces! Oh my!        
            if out == "(":
                PARENTH = 1
                if prev == ".":
                    tlOut = tlOut[:-1]
                    out = '{'
                if prev == "./BRACK":
                    out = '['
                if prev == "./BOLD":
                    out = '\033[1m' + '[' + '\033[0m'
            if out == ")":
                PARENTH = 0
                if prev == ".":
                    tlOut = tlOut[:-1]
                    out = '}'
                if prev == "./BRACK":
                    out = ']'
                if prev == "./BOLD":
                    out = '\033[1m' + ']' + '\033[0m'
            if out.isnumeric() and prev == "./CAP":
                out = "," + out
                
            # Lines, bars, rays, not statement to exclude long dashes
            if out[0] == "_" and out[1] != "_" : 
                if MUL:
                    tlOut += f'{out[1:]}({temp}'
                    out = ""
                    temp = ""
                    MUL = 0
                else:
                    tlOut = tlOut[:-1]
                    tlOut += f'{out[1:]}({prev})'
                    out = ""
            if out == " + " or out == " - " or out == u" \N{PLUS-MINUS SIGN} " or out == u" \N{MINUS-OR-PLUS SIGN}":
                if not prev.isalnum() and prev != u'\N{DEGREE SIGN}' and prev != u'\xa2' and prev != "$" and prev != " " or prev == "./BASE":
                    out = out.strip()
                if MUL: 
                    MUL = 0
            match CAP: 
                case 1:
                    out = out.capitalize()
                    CAP = 0
                case 2: 
                    out = out.capitalize()
            
            if item == "001100" and not FRACT:
                out = "/"
            prev = out
            if MUL and out.isalnum():
                temp += out
            else:
                tlOut += out
            i += (int) (len(item) / 6)
        if (iarr[i-1] == "000000"):
            SPC = 1
        else:
            SPC = 0
        for item in possible:
            #print(f"Checking {item}, length {len(item)}")
            #print(f"NEM: {NME}")
            
            if not chkFlags(item) or CONT:
                CONT = 0
                if NME and (item in nLib.keys() or item in nums.keys()):
                    NEM(item)
                    break
                elif not NME and item in bLib.keys():
                    UEB(item)
                    if not TRAN:
                        continue
                    break
                else: 
                    if len(item) == 6:
                        NME = not NME # Try other?
            else:
                i += (int) (len(item) / 6)
                prev = UEBFlags[item] if not NME else NEMFlags[item]
                break

            #print(tlOut)
    tlOut = tlOut.strip()
    f_out = open('transliterateOutput.txt', 'w')
    f_out.write(tlOut)
    f_out.close()
    #return tlOut[:-1]
    
    
""" 
with open('nemethTestCasetest.txt', 'w', encoding = 'utf-8') as out:
   with open('nemethTestCaseIn.txt', 'r') as test:
       for line in test:
           print(line)
           if line[0] == 'L':
               out.write(line)
           else:
               out.write(transliterateBin(line) + '\n') """



        
        
    
    
    