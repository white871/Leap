# Leap Raspberry Pi Code


=======
Original Authors: Joseph White (*white871@purdue.edu*) and Patrick Baysinger (*Graduated Spring 2024, patbaysing@gmail.com*)<br> <br>
This repository contains Python code for reading Hall Effect sensor outputs, UEB Grade 2 and Nemeth transliteration, reading rotary encoder outputs and line reading, connecting via ssh, outputting to a word document in real-time, and building the GUI for user-friendliness. <br> <br>
For more information regarding our progress and a more in-depth explanation on what we use in this project, look at the software transition document in Microsoft Teams.
## This code must be kept up to date with the code in the Raspberry Pi; you can copy files to and from the Raspberry Pi using an ssh connection.
### Connecting to the Raspberry Pi: 
- Chances are you probably would not be able to have the Pi connect to Purdue's Wifi, so most likely you will need to use a hotspot for connecting to the Raspberry Pi:
  - Setup the hotspot with the name *and* password set as **PiConfig**, therefore the Pi can automatically connect to the hotspot
  - The user uploading/downloading code from the Pi must be connected to this hotspot as well
  - You will also need the Pi's IP address (you can easily find this with an Android phone or a Windows computer by going into the hotspot settings, not sure about Apple products though)
- If you successfully connect, you will be prompted with a password to the Pi: "BestTeam"
### For uploading code to the Pi:
- When these files are changed, upload them to the Raspberry Pi
- Uploading a file to a Pi with the same exact name and directory as an existing file on the Pi will overwrite the file on the Pi. Do this so you don't have to mess with the files on the Pi's OS.
- To upload the files to the pi, open up terminal and use the following command: scp (file directory) "pi name"@(Raspberry Pi IP Address):~
  - "pi name" should be Leap, change this Readme if otherwise
### For downloading code to the Pi:
- To copy a file FROM the pi, open terminal and use the following command: scp (pi name)@(pi address):~/(directory on Pi) (directory on user's computer)
  - I recommend copying files from the Pi directly to your local Github repository folder to make updating the online repository a quicker process
### For building an EXE file
The simpler way (quicker but less secure, recommend for application testing): <br>
  - Download PyInstaller using "pip install PyInstaller"
  - Run "python -m PyInstaller --onefile --hidden-import tkinter -w leap.py" in the directory where leap.py is present.
  - Make sure you have all libraries in Client/leap.py to successfully build the .exe file. <br>
<!-- --> The lengthier way (takes longer, but creates a more secure application, recommend for finalizing application): <br> <br>
  - Download nuitka using "pip install nuitka" or "python -m pip install nuitka"
  - Make sure you installed all imported Python libraries in Client/leap.py
  - Run "python -m nuitka --standalone --onefile --enable-plugin=tk-inter --mingw64 --windows-icon-from-ico=leap.ico leap.py"
## If multiple people are working on the Leap code:
- Fork the repository so you can make updates to the code all you like. Make a pull request and upload the code when you're done to keep the main repository and the Pi updated. NOTE: I highly recommend working on separate code files overall, Github will not merge changes for one file from different users, only from one user. 
## If original authors are no longer on the team
- Fork the repository and treat that as the main repository, or just make a new repository with all the files and abandon/archive this repository
- Feel free to contact original authors (see emails under header) if further assistance is needed. 
## Folders:
**Internal Tests**: Program(s) for testing electrical components, only contains a testing program used for troubleshooting/testing to ensure that the hall effect PCB works as intended.<br>
**Rotary Encoding**: Contains code and output file for tracking a student's vertical position of a page using a rotary encoder.<br> 
**TestCode**: Contains code that is work-in-progress and/or is not needed for the Raspberry Pi's operations.<br>
**Transliteration**: Programs, dictionaries, and output text files for reading Brailler inputs and converting to text.<br>
**Client**: Python files used in building the .exe application <br>
**archive**: Past code that is no longer used

## Main Files:
**main.py**: Python file that creates the GUI using Tkinter and opens a local ssh connection to obtain the Raspberry Pi outputs wirelessly (see instructions on using a hotspot for connecting to the Rapsberry Pi)<br>
**leap.exe**: The application itself, currently in a soft delivery stage <br>
*Current version is v0.2.0*: 
- Fixed an issue where ssh would not connect due to naming the new Raspberry Pi username ("Leap" instead of "leap"...whoops.) <br>
- Fixed (mostly) an issue where Windows Defender would flag/delete application as a virus (See "For building an exe file"
Leap.exe past versions: <br>
- v0.1.0: First iteration - Allows user to connect to Raspberry Pi using a mobile hotspot connection on windows, opens Microsoft word to allow user to monitor real-time transliteration (only works for windows devices, win32com is a windows-exclusive library.)

