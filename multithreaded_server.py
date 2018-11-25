import socket
import sys
import traceback
from threading import Thread
import socket  # Import socket module
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
s.bind(('', port))  # Bind to the port
s.listen(5)  # Now wait for client connection.

def main():

    start_server()

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


def start_server():
    host = "127.0.0.1"
    port = 8888  # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # SO_REUSEADDR flag tells the kernel to reuse a local
    # socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)  # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()


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


def Update_Config(msg, ip=''):
    # msg seria el archivo de texto con todos los archivos que contiene la carpeta del cliente que realiza un update
    with open("config.json", "r+") as config:
        json_data = json.loads(json.loads(config.readline()))
        msg_data = json.loads(json.loads(msg))
        for file in msg_data:
            for value in msg_data[file]:
                if value not in json_data.key_values():
                    json_data[value] = []
                json_data[value].append(ip)
    config.close()
    return None


def client_thread(connection, ip, port, max_buffer_size=5120):
    is_active = True

    while is_active:
        client_input = receive_input(connection, max_buffer_size)

        if "--QUIT--" in client_input:
            print("Client is requesting to quit")
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
        else:
            print("Processed result: {}".format(client_input))
            connection.sendall("-".encode("utf8"))


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result


def process_input(input_str):
    print("Processing the input received from client")

    return "Hello " + str(input_str).upper()


if __name__ == "__main__":
    main()
