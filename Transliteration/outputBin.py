import ast

braille = input("Enter Braille input.\n")
with open('brailletobinary.txt', 'r', encoding = "utf-8") as b2b:
    B2B = b2b.read()
binary = ast.literal_eval(B2B)
out = ""
for grid in braille:
    out += binary[grid]
print(out)