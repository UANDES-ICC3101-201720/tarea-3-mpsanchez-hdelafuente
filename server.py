import socket
import sys
import traceback
from threading import Thread
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
    with open("config.json", "r") as config:
        json_data = json.loads(config.readline())
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
        config.close()
    config = open("config.json", "w")
    json.dump(json_data, config)    
    config.close()
    return None


def Search_File(file_name, config):
    clients = {}
    for file in config.keys():
        if file_name in file:
            clients[file] = config[file]
    return clients


def main():
    start_server()


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 12345  # Reserve a port for your service.

    print("socket created")

    try:
        s.bind(('', port))  # Bind to the port
    except:
        print("Bind failed. Error: " + str(sys.exc_info()))
        sys.exit()

    s.listen(5)  # Now wait for client connection.
    print("Socket now listening")

    while True:
        c, addr = s.accept()  # Establish connection with client.
        ip, port = str(addr[0]), str(addr[1])

        print('Got connection from', addr)

        try:
            Thread(target=client_thread, args=(c, ip)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    s.close()


def client_thread(c, ip):
    while True:
        try:
            c.send('[Server] Thank you for connecting'.encode())
        except:
            print("Error xD")
            break
        update_msg = c.recv(1024).decode()
        print("client: " + update_msg)
        if "Update" in update_msg:
            Update_Config(c.recv(1024).decode(), ip)
        exit = False
        while not exit:
            config = Read_Config()
            client_msg = c.recv(1024).decode()
            if "Exit" in client_msg:
                print("Ok")
                exit = True
                c.close()
                break
            client_msg = json.loads(client_msg)
            if client_msg["action"] == 1:
                search = Search_File(client_msg["keyword"], config)
                c.send(json.dumps(search).encode())
            elif client_msg["action"] == 2:
                Update_Config(c.recv(1024).decode(), ip)
            else:
                print("Unkown option")
                continue
    c.close()


if __name__ == "__main__":
    main()
