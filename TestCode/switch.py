import ast
import csv
import json

with open('brailletobinary.txt', 'r') as f:
    data = f.read()
b2b = ast.literal_eval(data)
#print(b2b)

reader = csv.reader(open('brailleStuff.csv', 'r'))
d = {}
for row in reader:
   k, v = row
   if not(k in d.keys()):
        d[k] = []
   d[k].append(v)
   
print(d)

newd = {}
for key in d:
    newkey = ""
    for char in key:
        try:
            newkey += b2b[char]
        except:
            continue
        
    newd[newkey] = d[key]
print(newd)

    

with open('braileLib.txt', 'w') as fi:
    fi.write(json.dumps(newd))
