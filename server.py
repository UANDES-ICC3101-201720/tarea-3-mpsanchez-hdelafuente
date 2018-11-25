import socket  # Import socket module
import json


def Send_File(file, c):
    c.send("[Server] Sending".encode())
    f = open(file, 'rb')
    l = f.read(1024)
    while l:
        print("Sending...")
        print(l)
        c.send(l)
        l = f.read(1024)
    f.close()
    print("Sent!")
    c.send("[Server] Done".encode())
    return None


def Read_Config():
    with open("config.json", "r+") as config:
    	print(config.readline())
    	json_data = {}
    config.close()
    return json_data


def Update_Config(msg, ip):
    # msg seria el archivo de texto con todos los archivos que contiene la carpeta del cliente que realiza un update
    with open("config.json", "r+") as config:
    	try:
    		json_data = json.loads(config.readline())
    	except Exception as e:
    		json_data = {}
    	msg_data = json.loads(msg)
    	for file in msg_data:
    		for value in msg_data[file]:
    			if value not in json_data.keys():
    				json_data[value] = []
    			if ip not in json_data[value]:
    				json_data[value].append(ip)
    	config.truncate(0)
    	json.dump(json_data, config)
    config.close()
    return None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
s.bind(('', port))  # Bind to the port
s.listen(5)  # Now wait for client connection.

while True:
    c, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    c.send('[Server] Thank you for connecting'.encode())
    update_msg = c.recv(1024).decode()
    print("client: " + update_msg)
    if "Update" in update_msg:
    	Update_Config(c.recv(1024).decode(), addr[0])
    
    exit = False
    while not exit:
    	config = Read_Config()
    	print("config: " + str(config))
    	client_msg = c.recv(1024).decode()
    	if "Exit" in client_msg:
    		print("Ok")
    		exit = True
    		break
    	client_msg = json.loads(client_msg)
    	if client_msg["action"] == 1:
    		print("atcion 1")
    	elif client_msg["action"] == 2:
    		print("action2")
    	elif client_msg["action"] == 3:
    		print("action 3")
    	else:
    		print("Unkown option")
    		continue


    c.close()
    # Desrialize json using:
    # 1: Search file
    # 2: Download file