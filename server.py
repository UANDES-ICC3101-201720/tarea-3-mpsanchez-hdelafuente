import socket  # Import socket module
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
s.bind(('', port))  # Bind to the port
s.listen(5)  # Now wait for client connection.


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
        json_data = json.loads(json.loads(config.readline()))
    config.close()
    return json_data


def Update_Config(msg):
    config = open("config.json", "r+")
    json.dump(msg, config)
    config.close()
    return None


while True:
    c, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)

    json_config = Read_Config()
    print("json_config:")
    print(type(json_config))

    c.send('[Server] Thank you for connecting'.encode())
    msg = c.recv(1024).decode()
    Update_Config(msg)

    # Desrialize json using:
    # 1: Search file
    # 2: Download file

    c.close()  # Close the connection
