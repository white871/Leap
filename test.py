"""
import ast

with open('UEBGrade2Lib', 'r') as f:
    data = f.read()
brailleLib = ast.literal_eval(data)
"""
while True:
    print("Enter Braille Binary String:")
    braille = input()
    if braille == 'q':
        break;
    if len(braille) != 6:
        print("Invalid, try again")
        continue
    