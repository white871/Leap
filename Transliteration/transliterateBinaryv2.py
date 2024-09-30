import ast
import time
import pdb
#import tracemalloc
start_time = time.time()
#tracemalloc.start()
# Open dictionaries

with open('brailleLib.txt', 'r') as bL: 
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
flags = {
    "001111" : "NUM",       # Numeric indicator
    "000100011100" : "NUM", # $
    "000100100100" : "NUM", # Cent symbol
    "111011" : "NUM",       # Opening Parenthesis
    "001101" : "NUM",       # Plus
    "001001" : "NUM",       
    "000111" : "PUN",   
    "000001" : "CAP",
    "000011" : "GD1",
    "100111" : "FRA",
}


def transliterateBin(inputB):
    global CAP, LEN, TRAN, NME, LIB, NUM, PUN, FRACT, SPC, CONT, bLib, nLib, tlOut, lastOut, i
    LIB = CAP = LEN = TRAN = NME = NUM = PUN = FRACT = SPC = CONT = 0
    global flags
    NME = 1 # Remove when ready to test mixed Braille
    tlOut = ""
    lastOut = ""
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
    possible = []
    i = 1
    while(i < len(iarr) - 1):
        possible = [None] * (len(iarr[i:]) if len(iarr) - i < 5  else 5)
        posLen = len(possible)
        print(f"LENGTH: {len(possible)}")
        for k in range(6, -1, -1):
            if k < posLen:
                possible[posLen - k - 1] = ("".join(iarr[i:i+k+1]))
        TRAN = 0
        
        #print(f"POSSIBLE: {possible}")
        def chkFlags(item):
            
            global PUN, CAP, NUM, FRACT, NME, CONT
            if item in nLib.keys():
                CONT = 1;
            else:
                CONT = 0;
            if item in flags.keys():
                print("Maybe a flag?")
                print(f"{flags[item]}, {FRACT}")
                PUN = 1 if flags[item] == "PUN" else 0
                CAP += 1 if (flags[item] == "CAP" and FRACT == 0) else CAP
                FRACT = 1 if flags[item] == "FRA" else 0
                FRACT = 0 if (flags[item] == "NUM" and FRACT == 1) else FRACT
                NUM = 1 if ((flags[item] == "NUM" and FRACT == 0) or FRACT == 1) else 0
                print(CAP)
                #print(PUN or CAP or NUM or FRACT)
                return (PUN or CAP or NUM or FRACT)
            return 0
            
            
        def UEB(item):
            global iarr
            for perhaps in bLib[item]:
                pass
                     
            

        def NEM(item):
            global tlOut, i, TRAN, NUM, CAP, SPC
            print(f"{item} passed, checking")
            #print(nLib[item])
            if item == '000000':
                SPC = 1
                NUM = 0
                CAP = 0
            else:
                SPC = 0
            TRAN = 1
            
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
            print(out)
            tlOut += out
            i += (int) (len(item) / 6)   

        for item in possible:
            print(f"Checking {item}, length {len(item)}")
            if TRAN == 0:
                if not chkFlags(item) or CONT:
                    print(f"Flag not found, or flag raised and {CONT}")
                    #print(f"{item} is not a flag.")
                    CONT = 0
                    if NME and (item in nLib.keys() or item in nums.keys()):
                        #print(f"Checking nemeth: {nLib[item]}")
                        NEM(item)
                    elif ~NME and item in bLib.keys():
                        #print(f"Checking UEB: {nLib[item]}")
                        UEB(item)
                else:
                    i += (int) (len(item) / 6)
                    print(f"Item is a flag...skipping")

            #print(tlOut)
    print(tlOut)
    
#pdb.set_trace()
braille = input("Input Binary input.\n")
transliterateBin(braille)  
#print("-------PROCESS COMPLETE--------------------------------------")         
print(f"PROCESS COMPLETED IN {(time.time() - start_time) * 1000} ms")
#print(f"MEMORY USAGE: {tracemalloc.get_traced_memory()}")
#tracemalloc.stop()



        
        
    
    
    