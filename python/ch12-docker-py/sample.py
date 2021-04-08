import docker

STREAM_HEADER_SIZE_BYTES = 8

client = docker.from_env()

def test_sample():	
	result = client.version()
	print(result)
	result = client.containers.list()
	print(result)

	result = client.images.pull('nginx:1.10-alpine')

	print(result)

	result = client.images.list()

	print(result)


def test_log():
	logs = client.containers.get('61709b0ed4b8').logs(stream=True)
	try:
		while True:
			line = next(logs).decode("utf-8")
			print(line)
	except StopIteration:
		print(f'log stream ended for {container_name}')   


def test_exec_ping():
	# ExecResult = namedtuple('ExecResult', 'exit_code,output')
	result = client.containers.get("2075").exec_run("ping www.weibo.cn", tty=True, stream=True)
	try:
		while True:
			line = next(result[1]).decode("utf-8")
			print(line)
	except StopIteration:
		print(f'exec stream ended for {container_name}')


def test_exec_bash():
	# ExecResult = namedtuple('ExecResult', 'exit_code,output')
	_, socket = client.containers.get("2075").exec_run("sh", stdin=True, socket=True)
	print(socket)
	socket._sock.sendall(b"ls -la\n")
	try:
		unknown_byte=socket._sock.recv(docker.constants.STREAM_HEADER_SIZE_BYTES)
		print(unknown_byte)

		buffer_size = 4096 # 4 KiB
		data = b''
		while True:
			part = socket._sock.recv(buffer_size)
			data += part
			if len(part) < buffer_size:
				# either 0 or end of data
				break
		print(data.decode("utf8"))

	except Exception: 
		pass
	socket._sock.send(b"exit\n")


if __name__ == "__main__":
    test_exec_bash()