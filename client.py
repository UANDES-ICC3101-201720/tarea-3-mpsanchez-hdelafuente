import socket               # Import socket module
import os
# http://cs.berry.edu/~nhamid/p2p/framework-python.html
#Ignore
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def Send_File(file_name, s): # This function sends a file to the socket
	f = open(file_name, 'rb')
	l = f.read(1024)
	while l:
		print("[Client] Sending...")
		s.send(l)
		l = f.read(1024)
	f.close()
	print("[Client] Sent!")
	print(s.recv(1024).decode()) # Server response
	return None

def Recive_File(file_name, s):
	return None


def Menu(s): # s: Socket
	print("\t1. Search file\n\t2. Download file\n\t3. Send file\n\t0. Exit")
	des = input("Option: ")
	if des == "1":
		file = input("File: ")
		msg = "Search " + file
		s.send(msg.encode())
		print(s.recv(1024).decode())
	elif des == "2":
		file = input("File: ")
		msg = "Download " + file
		s.send(msg.encode())
		print(s.recv(1024).decode())
		f = open(file,'wb')
		while (True):
			l = s.recv(1024)
			while (not " Done" in l.decode()):
				print("[Client] Recieving...")
				f.write(l)
			if " Done" in l.decode():
				print("linea 54")
				break
			print("aca")
		f.close()
	elif des == "3":
		file = input("File: ")
		Send_File(file, s)
	else:
		s.send("bye...".encode())
		return 1
	return None

if __name__ == "__main__":
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # Get local machine name
	port = 12345                # Reserve a port for your service.
	try:
		s.connect((host, port))
	except Exception as e:
		print("Connection refused\nExiting...")
		exit()
	print("Welcome " + str(host) + "!")
	print(s.recv(1024).decode())
	while True:
		Menu(s)
		if Menu(s) == 1:
			break

	s.close()                  # Close the socket when done