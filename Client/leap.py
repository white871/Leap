import tkinter
import paramiko
import scp
import win32com.client
import psutil
import binarytobraille
import win32gui

scp_client = None
ssh = None
server = None

def createSSHClient(server, port, user, password):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(server, port, user, password, timeout = 3.0)
	return client

def is_process_running(process_name):
	for process in psutil.process_iter(['pid', 'name']):
		if process.info['name'] == process_name:
			return True
	return False
	 
def connect():
	global scp_client
	global ssh
	global server
	global status
	global login
	global enterBt
	global ip_entry
	if (is_process_running("WINWORD.EXE")):
		status.config(text = "Please close all word tabs before creating new doc.")
	else:
		status.config(text = "Connecting...")
		login.update()
		server = ip_entry.get()
		try:
			ssh = createSSHClient(server, 22, "leap", "BestTeam")
			ssh.invoke_shell()
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('/bin/bash -lc "cd Transliteration; python transliteration.py"')
			scp_client = scp.SCPClient(ssh.get_transport(), socket_timeout = 3.0)
			status.config(text = "Connected! Please close all Word tabs to create new doc. (Make sure to save your progress.)")
			login.update_idletasks()
			edit_word()
		except Exception as e: 
			status.config(text = 'Failed. Please check hotspot settings to ensure IP is correct and brailler is still connected.')
			login.update_idletasks()

def edit_word():
	global scp_client
	global ssh
	global server
	login.destroy()
	word = win32com.client.gencache.EnsureDispatch('Word.Application')
	braille_doc = word.Documents.Add()
	ascii_doc = word.Documents.Add()
	word.Visible = True
	word.WindowState = win32com.client.constants.wdWindowStateMaximize
	ascii_doc.Sections(1).Headers(win32com.client.constants.wdHeaderFooterPrimary).Range.Text = server + " Alpha-Numeric"
	braille_doc.Sections(1).Headers(win32com.client.constants.wdHeaderFooterPrimary).Range.Text = server + " Braille"
	while (True):
		try:
			print("trying again")
			scp_client.get("~/Transliteration/transliterateOutput.txt")
			scp_client.get("~/Transliteration/tempBin.txt")
			print("here:(")
			f_scp_ascii = open("transliterateOutput.txt", "r")
			f_scp_braille = open("tempBin.txt")
			ascii_doc.Content.Text = f_scp_ascii.read()
			ascii_doc.Content.Font.Size = 16
			braille_doc.Content.Text = binarytobraille.binToBraille(f_scp_braille.read())
			braille_doc.Content.Font.Size = 16
			print("herekdkd")
			ssh.get_transport().set_keepalive(60)
		except Exception as e:
			print(str(e))
			if 'None' in str(e):
				on_closing()
				exit()
			else:
				pass

def on_closing():
	global ssh
	global enterBt
	ssh.exec_command('/bin/bash -lc "pkill -f transliteration"')
	ssh.exec_command('/bin/bash -lc "pkill -f encoder"')
	exit()


def to_login(): # Sequence 1
	global no_win
	global inputtxt
	global login
	global status
	global enterBt
	global win
	global ip_entry
	win.destroy()
	if not no_win:
		no_win = True
		login = tkinter.Tk()
		login.geometry('1500x200')
		login.title("Login")
		
		prompt = tkinter.Label(login, text = 'Enter Device IP Address', font = ('Calibri 20 bold'))
		prompt.pack()
		ip_entry = tkinter.StringVar()
		inputtxt = tkinter.Entry(login, width = 90, font = 'Calibri 20', textvariable = ip_entry)
		inputtxt.pack()
		inputtxt.bind("<Return>", lambda e: connect())
		enterBt = tkinter.Button(login, text = 'Create New Doc', command = connect, font = 'Calibri 18')
		enterBt.pack()
		status = tkinter.Label(login, text = " ", font = "Calibri 18")
		status.pack(pady = 1)
	
win = tkinter.Tk()
win.title('Leap Transliteration Reader v 0.1.0')
win.geometry('720x480')

label1 = tkinter.Label(win, text = 'Leap Transliteration Reader v 0.1.0', font = ('Calibri 20 bold'))
label2 = tkinter.Label(win, text = "Please read the following below before continuing!", font = ('Calibri 15 bold'))
label3 = tkinter.Label(win, text = 'To begin, you will need to create a hotspot on your computer. For Windows 10: open settings, open Network & Internet, then Mobile Hotspot. Edit the network name and password to "PiConfig", then switch the Mobile Hotspot "on". When the device is connected, the IP Address should show up on the window on your computer: copy it down.', wraplength = 600, font = ('Calibri 15'))
label1.pack(pady = 20)
label2.pack(pady = 20)
label3.pack(pady = 20)

button1 = tkinter.Button(win, text = 'I have read the following information above.', command = to_login, font = "Calibri 18")
button1.pack(pady = 30)
no_win = False
win.mainloop()
