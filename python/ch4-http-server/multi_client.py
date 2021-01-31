import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    for x in range(10):
        sock.sendall(b'Hello, world')
        data = sock.recv(1024)
        print('Received', repr(data))
        time.sleep(1)