import socket               # Import socket module
import os
import json
from threading import Thread

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

def Send_File(file_name, s): # This function sends a file to the socket
	f = open(file_name, 'rb')
	l = f.read(1024)
	while l:
		s.send(l)
		l = f.read(1024)
	f.close()
	s.send("Done".encode())
	return None

def Recive_File(file, s):
	f = open(file,'wb')
	l = s.recv(1024)
	while (not "Done" in l.decode()):
		f.write(l)
	f.close()
	return None


def Menu(s): # s: Socket
	msg_to_server = {}
	print("\t1. Search file\n\t2. Update files\n\t0. Exit")
	des = input("Option: ")
	if des == "1":
		file = input("File: ")
		msg_to_server["action"] = 1
		msg_to_server["keyword"] = file
		s.send(json.dumps(msg_to_server).encode())
		search = json.loads(s.recv(1024).decode())
		print(search)
		to_download = input("Wich one: ")
		cnt = 0
		if search[to_download][cnt] == "192.168.0.130":
			cnt += 1
		try:
			Thread(target = P2P_Recv, args = (to_download, search[to_download][cnt])).start()
		except Exception as e:
			print("Error en recv")
			print(e)
	elif des == "2":
		msg_to_server["action"] = 2
		s.send(json.dumps(msg_to_server).encode())
		files = os.listdir()
		data = {}
		data[host] = []
		for i in files:
			data[host].append(i)
		json_data = json.dumps(data)
		s.send(json_data.encode())
	else:
		s.send("Exit".encode())
		s.close()
		exit()
	return None

def Update_Files(s, host):
	files = os.listdir()
	data = {}
	data[host] = []
	for i in files:
		data[host].append(i)
	json_data = json.dumps(data)
	# Send this updated information to server
	try:
		s.send(json_data.encode("utf-8"))
		print("Sending info.")
	except Exception as e:
		print("Error updating file info")
		print(e)
		s.close()

	try:
		Thread(target = P2P_Send, args = ()).start()
	except Exception as e:
		print("Error en send")
		print(e)


	return None

def P2P_Recv(file_name, host):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = 8888
	s.connect((host, port))
	s.send(file_name.encode())
	msg = s.recv(1024).decode()
	if "Starting" in msg:
		Recive_File(file_name, s)

	
	s.close()
	return None

def P2P_Send():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = 8888
	s.bind(('', port))
	s.listen(5)
	while True:
		c, addr = s.accept()
		file_name = c.recv(1024).decode()
		s.send("Starting".encode())
		Send_File(file_name, s)

	s.close()
	return None


if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
	host = socket.gethostname() # Get local machine name
	port = 12345               # Reserve a port for your service.
	try:
		s.connect(("192.168.0.171", port))
	except Exception as e:
		print("Connection refused\nExiting...")
		exit()
	print("Welcome " + str(host) + "!")
	print(s.recv(1024).decode())
	s.send("Update".encode())
	Update_Files(s, host)
	while True:
		Menu(s)
	s.shutdown()
	s.close()                  # Close the socket when done