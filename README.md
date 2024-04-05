# Leap Raspberry Pi Code
*Last updated: 4/5/2024*

This repository contains Python code for reading Hall Effect sensor outputs, UEB Grade 2 transliteration, reading rotary encoder outputs and line reading, 

## This code must be kept up to date with the code in the Raspberry Pi, therefore you can copy files to and from the Raspberry Pi
### Connecting to the Raspberry Pi: 
- Chances are you probably would not be able to have the Pi connect to Purdue's Wifi, so most likely you will need to use a hotspot for connecting to the Raspberry Pi:
  - Setup the hotspot with the name *and* password set as **PiConfig**, therefore the Pi can automatically connect to the hotspot
  - The user uploading/downloading code from the Pi must be connected to this hotspot as well
  - You will also need the Pi's IP address (you can easily find this with an Android phone by going into the hotspot settings, not sure about an iPhone though)
- If you successfully connect, you will be prompted with a password to the Pi: "BestTeam"
### For uploading code to the Pi:
- When these files are changed, upload them to the Raspberry Pi
- Uploading a file to a Pi with the same exact name and directory as an existing file on the Pi will overwrite the file on the Pi. Do this so you don't have to mess with the files on the Pi's OS.
- To upload the files to the pi, open up terminal and use the following command: scp (file directory) "pi name"@(Raspberry Pi IP Address):~
  - "pi name" should be Leap, change this Readme if otherwise
### For downloading code to the Pi:
- To copy a file FROM the pi, open terminal and use the following command: scp (pi name)@(pi address):~/(directory on Pi) (directory on user's computer)
  - I recommend copying files from the Pi directly to your local Github repository folder to make updating the online repository a quicker process
## If multiple people are working on the Leap code:
- Fork the repository so you can make updates to the code all you like. Make a pull request and upload the code when you're done to keep updated on the main repository and the Pi.
  



