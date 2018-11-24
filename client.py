import socket               # Import socket module
import os
import json

"""
mensaje cliente a servidor
{
	"action" : [1,2,3],
	"keyword": /*nombre del archivo*/
}

respuesta postiva del server
{
	"response" : True
	"Files" : [ { /* Hash* /:
			{	"name": /*nombre del archivo*/
				"size" : float
				"peers" : int
			}
		}
	]
}

respuesta negativa del server

{
	"response" : False
	"error" : "sapo qlo busca una wea que exista"
}

si la repsuesta es afirmativa, 
el cliente selecciona las wea que quiere bajar, 
y el server le da los ip.

"""

# http://cs.berry.edu/~nhamid/p2p/framework-python.html
# Ignore
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

def Recive_File(file, s):
	f = open(file,'wb')
	while (True):
		l = s.recv(1024)
		while (not " Done" in l.decode()):
			print("[Client] Recieving...")
			f.write(l)
		if " Done" in l.decode():
			#print("linea 54")
			break
	f.close()
	return None


def Menu(s): # s: Socket
	msg_server = {}
	print("\t1. Search file\n\t2. Download file\n\t3. Send file\n\t0. Exit")
	des = input("Option: ")
	if des == "1":
		file = input("File: ")
		msg_server["action"] = 1
		msg_server["keyword"] = file
		s.send(json.dumps(msg_server).encode())
		print(s.recv(1024).decode()) #Json
	elif des == "2":
		file = input("File: ")
		msg_server["action"] = 2
		msg_server["keyword"] = file
		s.send(json.dumps(msg_server).encode())
		print(s.recv(1024).decode())
		
	elif des == "3":
		file = input("File: ")
		Send_File(file, s)
	else:
		s.close()
		exit()
	return None

def Update_Files(s, host):
	files = os.listdir()
	data = {}
	data[host] = []
	for i in files:
		data[host].append(i)
	json_data = json.dumps(data).encode()
	# Send this updated information to server
	try:
		s.send(json_data)
	except Exception as e:
		print("Error updating file info")
		print(e)
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
	Update_Files(s, host)
	while True:
		Menu(s)

	s.close()                  # Close the socket when done