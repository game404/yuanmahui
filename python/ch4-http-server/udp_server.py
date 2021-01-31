import socket

HOST = 'localhost'
PORT = 65432

with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as sock:  # type不一样
    # Bind the socket to the port
    sock.bind((HOST, PORT))
    while True:
        data, address = sock.recvfrom(4096)  # 直接接收数据
        print("recv data", data, address)
        if data:
            sock.sendto(data, address)  #  sendto 发送到制定地址

