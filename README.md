# LeapHallEffect
Python code for reading Hall Effect outputs and translating Braille. Library for translation is included.

- When these files are changed, upload them to the Raspberry Pi (you should probably remove the current copy on the Pi as well)
- To upload the files to the pi, open up terminal and use the following command: scp (file directory) "pi name"@(Raspberry Pi IP Address):~
 - The Pi must be on and connected to the network.
- To copy a file FROM the pi, open terminal and use the following command: scp (pi name)@(pi address):~/(file name) (directory to be copied to)


Files included:
- UEBGrade2Lib is no longer used, and will be most likely removed in the future, brailleLib.txt is the braille library dictionary in use
- Extra files: brailleStuff.csv is a spreadsheet of braille grids to text, brailletobinary.txt is a dictionary of conversions from braille grid to a 6-bit string
- Test.py is a test program for manually entering a binary string to imitate using the Brailler
- translation.py is the test program used for the ISBVI visit in Spring 2024, currently it's only used for brailler reading and grade 1 testing with the Raspberry Pi
- demofile.txt is the output text file of translation.py
- newTranslation.py is a prototype of UEB grade 2 transliteration, this is currently a "work in progress" program


