import socket


def listen(port,buffersize):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.bind(("127.0.0.1", port))
    
    
    while 1:
        data,addr = serversocket.recvfrom(buffersize)
    
        print ("Received from: {0} data: {1}".format(addr, data.decode()))
        message = "Message received successfully: {0}".format(data.decode())
        serversocket.sendto(message.encode(), addr)

def main():
    listen(9600, 1024)

if __name__ == "__main__":
    main()