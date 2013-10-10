import socket



#create an INET, STREAMing socket
def create_connection(port, buffersize):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientsocket.connect(('127.0.0.1', port))
    
    
    i=0
    while i < 100:
        message = "Test {0}".format(i)
        clientsocket.send(message.encode())
        received = clientsocket.recv(buffersize)
        clientsocket.send
        print(received.decode())
        i = i + 1
    
    
    clientsocket.close()
                         
def main():
    create_connection(9600, 1024)

if __name__ == "__main__":
    main()
