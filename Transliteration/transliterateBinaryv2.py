import ast
import time
import pdb
#import tracemalloc

#tracemalloc.start()
# Open dictionaries

with open('UEBLib.txt', 'r') as bL: 
    bLdata = bL.read()
bLib = ast.literal_eval(bLdata)

""" with open('brailletobinary.txt', 'r', encoding = "utf-8") as f:
    bbD = f.read()
b2b = ast.literal_eval(bbD) """

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
  "000001" : ","
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
    "001111" : "./NUM",       # Numeric indicator
    "000100011100" : "./NUM", # $
    "000100100100" : "./NUM", # Cent symbol
    "111011" : "./NUM",       # Opening Parenthesis
    "001101" : "./NUM",       # Plus
    "001001" : "./NUM",       # Minus
    "000111" : "./PUN",   
    "000001" : "./CAP",
    "000011" : "./GD1",
    "100111" : "./FRA",
    "000111" : "./MIX",
    "000111100011" : "./NEM", # Closing nemeth indicator
    "000001001000" : "./SWI",
    "000110" : "./SUP",
    "000010" : "./BASE",
    
    
    
}
UEBFlags = {
    "000011" : "./GD1",
    "000011001000" : "./GD1TERM",
    "000001" : "./CAP",
    "000001001000": "./CAPTERM"
}


def transliterateBin(inputB):
    global \
        CAP, LEN, TRAN, NME, LIB, NUM, PUN, FRACT, \
        SPC, CONT, MIX, GD1, SUP, \
        bLib, nLib, tlOut, prev, i, iarr
    LIB = CAP = LEN = TRAN = NME = SUP = NUM = PUN = FRACT = SPC = CONT = MIX = GD1 =  0
    global flags
    NME = 1 # Remove when ready to test mixed Braille
    tlOut = ""
    prev = ""
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
    print(f"Input array: {iarr}")
    possible = []
    i = 1
    while(i < len(iarr)):
        possible = [None] * (len(iarr[i:]) if len(iarr) - i < 5  else 5)
        posLen = len(possible)
        print(f"LENGTH: {len(possible)}")
        for k in range(6, -1, -1):
            if k < posLen:
                possible[posLen - k - 1] = ("".join(iarr[i:i+k+1]))
        
        #print(f"POSSIBLE: {possible}")
        def chkFlags(item):
            
            global PUN, CAP, NUM, FRACT, NME, CONT, MIX, GD1, SUP
            if item in nLib.keys():
                CONT = 1;
            else:
                CONT = 0;
                #print(f"{flags[item]}, {FRACT}")
            if not NME and item in UEBFlags.keys():
                CAP += 1 if UEBFlags[item] == "./CAP" else CAP
                GD1 = 1 if UEBFlags[item] == "./GD1" else 0
                return (CAP or GD1)
            if NME and item in NEMFlags.keys():
                CAP += 1 if (NEMFlags[item] == "./CAP" and FRACT == 0) else CAP
                NUM = 1 if ((NEMFlags[item] == "./NUM" and FRACT == 0) or FRACT == 1) else NUM
                PUN = 1 if NEMFlags[item] == "./PUN" else 0
                FRACT = 1 if NEMFlags[item] == "./FRA" else FRACT
                FRACT = 0 if (NEMFlags[item] == "./NUM" and FRACT == 1) else FRACT
                MIX = 1 if NEMFlags[item] == "./MIX" else MIX
                SUP = 1 if NEMFlags[item] == "./SUP" else SUP
                SUP = 0 if NEMFlags[item] == "./BASE" else SUP
                #print(CAP)
                #print(PUN or CAP or NUM or FRACT)
                return (PUN or CAP or NUM or FRACT or GD1 or MIX or SUP)
            return 0
            
            
        def UEB(item):
            global iarr, i, tlOut, TRAN, CAP, GD1, prev
            spec = 1 # Do all elements have _ or ^?
            TRAN = 0
            if item == "000000" and CAP == 2:
                CAP = 0
            spaceBefore = (iarr[i - 1] == "000000" or iarr[i - 1] in UEBFlags.keys())
            spaceAfter = (iarr[i + (int)(len(item) / 6)] == "000000" or iarr[i + (int)(len(item) / 6)] in UEBFlags.keys())
            for perhaps in bLib[item]:
                print(perhaps)
                if not TRAN and not GD1:
                    if "_" in perhaps:
                        print("_ found")
                        if spaceBefore and spaceAfter:
                            print("_ passed")
                            out = perhaps.replace("_","")
                            TRAN = 1
                        if iarr[i + (int)(len(item) / 6)] in bLib.keys():
                            if (iarr[i - 1] == "000000" or "./" in prev) and (not bLib[iarr[i + (int)(len(item) / 6)]][0].replace("^", "").replace("_", "").isalnum()):
                                print("_ passed (2nd)")
                                out = perhaps.replace("_","")
                                TRAN = 1
                    elif perhaps[0] == '^' and perhaps[-1] == '^':
                        if not spaceBefore and not spaceAfter:
                            out = perhaps.replace("^", "")
                            TRAN = 1
                    elif perhaps[0] == '^': 
                        if not spaceBefore:                           
                            out = perhaps.replace("^", "")
                            TRAN = 1
                    elif perhaps[-1] == '^':
                        if not spaceAfter:
                            out = perhaps.replace("^", "")
                            TRAN = 1
                    else:
                        spec = 0
            print(f"TRAN: {TRAN}, SPEC: {spec}")
            if not TRAN and (not spec or len(item) == 6):
                print("Final say")
                out = bLib[item][0].replace("_", "").replace("^","")
                TRAN = 1
            
            if TRAN:
                match CAP: 
                    case 1:
                        out = out.capitalize()
                        CAP = 0
                    case 2: 
                        out = out.upper()
                prev = out
                tlOut += out
                i += (int)(len(item) / 6)
            print(tlOut)

        def NEM(item):
            global tlOut, i, TRAN, NUM, CAP, SPC, SUP
            print(f"{item} passed, checking")
            #print(nLib[item])
            print(SUP)
            if item == '000000':
                SPC = 1
                NUM = 0
                CAP = 0
                if SUP:
                    tlOut += ")"
                SUP = 0
            else:
                SPC = 0
            TRAN = 1
            #print(f"NUM: {NUM}")
            if NUM and item in nums.keys(): 
                out = nums[item]
            else:
                out = nLib[item]
            
            match CAP: 
                case 1:
                    out = out.capitalize()
                    CAP = 0
                case 2: 
                    out = out.capitalize()
            #if SUP:
            #    tlOut += "^" + out
            #else:
            print(out)
            tlOut += out
            
            i += (int) (len(item) / 6)
            
        for item in possible:
            print(f"Checking {item}, length {len(item)}")
            if not chkFlags(item) or CONT:
                #print(f"Flag not found, (or flag raised but continue is {CONT})")
                    #print(f"{item} is not a flag.")
                CONT = 0
                if NME and (item in nLib.keys() or item in nums.keys()):
                        #print(f"Checking nemeth: {nLib[item]}")
                    NEM(item)
                    break
                elif not NME and item in bLib.keys():
                        #print(f"Checking UEB: {nLib[item]}")
                    UEB(item)
                    if not TRAN:
                        print("Not found!")
                        continue
            else:
                i += (int) (len(item) / 6)
                prev = UEBFlags[item] if not NME else NEMFlags[item]
                print(f"Item is a flag {prev}")

            #print(tlOut)
    print(tlOut)
    
#pdb.set_trace()
braille = input("Input Binary input.\n")
#braille = "000001011101000000101100100000101111101010111010000000010111000000111000100000110000101010111010000000111111000000111101000000011111000000011101000000111100000000111011000000011101000000111001010100111000111000100000110110100010"
start_time = time.time()
transliterateBin(braille)  
#print("-------PROCESS COMPLETE--------------------------------------")         
print(f"PROCESS COMPLETED IN {(time.time() - start_time) * 1000} ms")
#print(f"MEMORY USAGE: {tracemalloc.get_traced_memory()}")
#tracemalloc.stop()



        
        
    
    
    