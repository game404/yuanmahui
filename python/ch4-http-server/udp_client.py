# udp-client
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Create a UDP socket
with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:
    # Send data
    sock.sendto(b'Hello, world', (HOST, PORT))
    # Receive response
    data, server = sock.recvfrom(4096)
    print("recv data", data, server)