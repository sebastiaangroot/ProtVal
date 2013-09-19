def getModuleName():
    return "DNS Client Validator"

def getModuleDescription():
    return "A dummy DNS Client Validator"

def initMod():
    print("Inside DNS Client validator")

import socket

#create an INET, STREAMing socket
def create_connection(user_input, port, buffersize):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientsocket.connect((user_input, port))
    
    
    i=0
    while i < 100:
        message = "Test {0}".format(i)
        clientsocket.send(message.encode())
        received = clientsocket.recv(buffersize)
        print(received.decode())
        i = i + 1
    
    
    clientsocket.close()
                         
def main():
    user_input = input("Which DNS-server do you want to validate?")
    create_connection(user_input, 9600, 53)

if __name__ == '__main__':
    main()