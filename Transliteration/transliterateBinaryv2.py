import ast

# Open dictionaries
with open('brailleLib.txt', 'r') as bL: 
    bLD = bL.read()
bLib = ast.literal_eval(bLD)

with open('brailletobinary.txt', 'r', encoding = "utf-8") as bb:
    bbD = bb.read()
b2b = ast.literal_eval(bbD)

with open('nemethLib.txt', 'r') as nL:
    nLD = nL.read()
nLib = ast.literal_eval(nLD)

flags = {
    "001111" : "NUM",
    "000111" : "PUN",
    "000001" : "CAP",
    }


def transliterateBin(inputB):
    global CAP, LEN, TRAN, NME, LIB, NUM, PUN, FRACT, SPC, bLib, b2b, nLib, tlOut, lastOut, i
    LIB = CAP = LEN = TRAN = NME = NUM = PUN = FRACT = SPC = 0
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
    pos = []
    i = 1
    while(i < len(iarr) - 1):
        pos = [None] * (len(iarr[i:]) if len(iarr) - i < 5  else 5)
        posLen = len(pos)
        print(f"LENGTH: {len(pos)}")
        for k in range(6, -1, -1):
            if k < posLen:
                pos[posLen - k - 1] = ("".join(iarr[i:i+k+1]))
        TRAN = 0
        print(f"POS: {pos}")
        def chkFlags(item):
            global PUN, CAP, NUM, FRACT, NME
            if item in flags.keys():
                PUN = 1 if flags[item] == "PUN" else 0
                CAP = 1 if (flags[item] == "CAP" and FRACT == 0 and NME == 0) else 0
                NUM = 1 if flags[item] == "NUM" else 0
                FRACT = 1 if flags[item] == "FRA" else 0
                return (PUN or CAP or NUM or FRACT)
            return 0
            
            
        def UEB(item):
            
            pass

        def NEM(item):
            global tlOut, i, TRAN
            print(nLib[item])
            if item == '000000':
                NUM = 0

            if(item in nLib.keys()):
                out = ""
                TRAN = 1
                tlOut += nLib[item]
                i += (int) (len(item) / 6)
        
        for item in pos:
            if (item in bLib.keys() or item in nLib.keys()) and TRAN == 0:
                print(f"{item} passed")
                TRAN = 0
                if not chkFlags(item):
                    if (NME):
                        NEM(item)
                    else:
                        UEB(item)
                else:
                    i += 1

    print(tlOut)
    

transliterateBin("001111011000001011000000000101010000000000001111010011000110000101100001")           





        
        
    
    
    