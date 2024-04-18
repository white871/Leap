import tkinter as t
import paramiko as pm
from scp import SCPClient

server = input("Enter address of LEAP client: ")
port = 22
user = "leap"
password = "BestTeam"
window = None

def createSSHClient(server, port, user, password):
	client = pm.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(pm.AutoAddPolicy())
	client.connect(server, port, user, password)
	return client

def on_closing():
	global ssh
	print("Closing Window.")
	ssh.exec_command('/bin/bash -lc "pkill -f transliteration"')
	ssh.exec_command('/bin/bash -lc "pkill -f encoder"')
	window.destroy()

def gui(filename):
	global window
	window = t.Tk()
	window.title("Leap Output")
	output = t.Text(window, wrap = 'word', width = 40, height = 10)
	output.pack()

	outText = t.Label(output, text = "Hang on...")
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

ssh = createSSHClient(server, port, user, password)
ssh.invoke_shell()
stdin, stdout, stderr = ssh.exec_command('/bin/bash -lc "cd Transliteration; python transliteration.py"')
scp = SCPClient(ssh.get_transport())
gui("transliterateOutput.txt")