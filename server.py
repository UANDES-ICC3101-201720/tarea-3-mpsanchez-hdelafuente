import socket  # Import socket module

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(5)  # Now wait for client connection.

while True:
    c, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    c.send('[Server] Thank you for connecting'.encode())
    msg = c.recv(1024).decode()
    if "Download " in msg:
    	c.send("[Server] Sending".encode())
    	f = open(msg[9:], 'rb')
    	l = f.read(1024)
    	while l:
    		print("Sending...")
    		print(l)
    		c.send(l)
    		l = f.read(1024)
    	f.close()
    	print("Sent!")
    	c.send("[Server] Done".encode())
    if "Search " in msg:
    	msg_list = msg.split()
    	try:
    		temp = open(msg_list[1], 'rb')
    	except Exception as e:
    		c.send("[Server] File not in network")
    		continue
    	c.send("[Server] Print clients".encode())
    c.close()  # Close the connection

