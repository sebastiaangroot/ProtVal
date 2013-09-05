import socket

def sendmsg(address, port, message):
	buffer_size = 1024

	if type(message) == type(""):
		message = message.encode()

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(message, (address, port))
	data = (s.recv(buffer_size)).decode()
	s.close()
	print(data)

def main():
	sendmsg('127.0.0.1', 9500, 'Hello sockets')

if __name__ == "__main__":
	main()
