# Testing for translation without having to use the Raspberry Pi
# Enter the binary braille keys manually
import re
import ast

with open('braileLib.txt', 'r') as f:
    data = f.read()
lib = ast.literal_eval(data)
#print(lib)
output = []
while True:
    print("Enter Braille Binary String:")
    braille = input()
    if braille == 'q':
        break;
    if len(braille) != 6 or not(re.match('10', braille)):
        print("Invalid, try again")
        continue
    
    output.append(lib[braille])
    print(output)
print(braille)    
        