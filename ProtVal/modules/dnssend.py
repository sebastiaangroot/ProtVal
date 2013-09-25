import socket, dnspacket
buffer_size = 1024

p = dnspacket.DNSPacket()
p.setHeaderID(0b10011001)
p.setHeaderRD(1)
p.setHeaderQDCOUNT(1)
i = p.createQuestionSection()
p.addQuestionQNAME('test.iamotor.nl', i)
p.addQuestionQTYPE(1, i)
p.addQuestionQCLASS(1, i)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(p.getPacketBytes(), ('85.12.6.41', 53))
data = s.recv(buffer_size)
s.close()
print("Received:",data)