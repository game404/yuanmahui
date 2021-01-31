import socket
import selectors
HOST = '127.0.0.1'
PORT = 65432

sel = selectors.DefaultSelector()

def accept(sock, mask):  # 接受新连接
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)  # 继续加入selector

def read(conn, mask):  # 读取数据
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

serverd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverd.bind((HOST, PORT))
serverd.listen(100)
serverd.setblocking(False)  # 非阻塞
sel.register(serverd, selectors.EVENT_READ, accept)  # 只注册read事件

while True:  # 无限循环持续监听
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)