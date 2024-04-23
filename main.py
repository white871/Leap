from tkinter import *
import paramiko as pm
from scp import SCPClient


def createSSHClient(server, port, user, password):
	client = pm.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(pm.AutoAddPolicy())
	client.connect(server, port, user, password)
	return client
     
def connect():
    status.config(text = "Connecting...")
    server = inputtxt.get(1.0, 'end')
    try:
        ssh = createSSHClient(server, 22, "leap", "BestTeam")
        ssh.invoke_shell()
        stdin, stdout, stderr = ssh.exec_command('/bin/bash -lc "cd Transliteration; python transliteration.py"')
        scp = SCPClient(ssh.get_transport())
        status.config(text = "Connected!")
        gui('transliterateOutput.txt', scp)
    except:
        status.config(text = 'Connection Failed.')
    
	
def on_closing():
	global ssh
	status.config(text = "Closing Window")
	ssh.exec_command('/bin/bash -lc "pkill -f transliteration"')
	ssh.exec_command('/bin/bash -lc "pkill -f encoder"')
	window.destroy()

def to_login(): # Sequence 1
    global no_win
    global inputtxt
    global login
    global status
    #button1.destroy()
    if not no_win:
        no_win = True
        login = Toplevel(win)
        login.geometry('500x100')
        login.title("Login")
        prompt = Label(login, text = 'Enter Device IP Address')
        prompt.pack()
        inputtxt = Text(login, height = 1, width = 30)
        inputtxt.pack()
        enterBt = Button(login, text = 'Enter', command = connect)
        enterBt.pack()
        status = Label(login, text = " ")
        status.pack(pady = 1)
		
def gui(filename, scp):
	global window
	window = Tk()
	window.title("Leap Output")
	output = Text(window, wrap = 'word', width = 40, height = 10)
	output.pack()

	outText = Label(output, text = "Hang on...")
	outText.grid(row = 1, column = 1)
	window.minsize(400,400)
	def readOut():
		try:
			scp.get("~/Transliteration/transliterateOutput.txt")
		except:
			pass
		with open(filename, "r") as f:
			filecontent = f.read()
			outText.config(text = filecontent)
		window.after(3000, readOut)

	readOut()
	window.protocol("WM_DELETE_WINDOW", on_closing)
	window.mainloop()
	
win = Tk()
win.title('Leap Transliteration Reader v 0.1.0')
win.geometry('720x480')

label1 = Label(win, text = 'Leap Transliteration Reader v 0.1.0', font = ('Calibri 20 bold'))
label2 = Label(win, text = "Please read the following below before continuing!", font = ('Calibri 15 bold'))
label3 = Label(win, text = 'To begin, you will need to create a hotspot on your computer. For Windows 10: open settings, open Network & Internet, then Mobile Hotspot. \
Enable Share Connection with Other Devices, and edit the network name and password to "PiConfig", when the device is connected, the IP Address should show up on the window on your computer: copy it down.', wraplength = 600, font = ('Calibri 15'))
label1.pack(pady = 20)
label2.pack(pady = 20)
label3.pack(pady = 20)

button1 = Button(win, text = 'I have read the following information above.', command = to_login)
button2 = Button(win, text = 'Exit', command = lambda: win.destroy())
button2.pack(padx = 20)
button1.pack(pady = 30)
#win.after(3000, lambda: button1.config(state = 'normal'))
no_win = False
win.mainloop()