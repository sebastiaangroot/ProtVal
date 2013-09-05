import socket

def recvmsg(port):
	buffer_size = 1024
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('127.0.0.1', port))

	data, addr = s.recvfrom(buffer_size)

	print("Received data: " + data.decode())
	s.sendto(data, addr)
	s.close()

def main():
	recvmsg(9500)

if __name__ == "__main__":
	main()
