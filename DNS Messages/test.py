import math
import socket

def appendByteArray(array, value):
	if type(value) == type(int()):
		if value == 0:
			bytelen = 1
		else:
			bytelen = math.ceil(value.bit_length() / 8)
		new_array = array + value.to_bytes(bytelen, "big")
		return new_array
	elif type(value) == type(str()):
		new_array = array + value.encode()
		return new_array
	else:
		print('appendByteArray only takes <int> or <str> types')
		return array


def getStandardQuery():
	#Header section
	message = (0b0100010001000100).to_bytes(2, "big")
	qr_to_ra = 0b1 #RD: Yes
	qr_to_ra += 0b00 #TC: No
	qr_to_ra += 0b000 #AA: No
	qr_to_ra += 0b0000000 #OPCODE: Standard Query
	qr_to_ra += 0b00000000 #QR: Query	
	message = appendByteArray(message, qr_to_ra)
	ra_to_rcode = 0b0000 #RCODE: Empty
	ra_to_rcode += 0b0000000 #Z: Empty
	ra_to_rcode += 0b00000000 #RA: No
	message = appendByteArray(message, ra_to_rcode)
	message = appendByteArray(message, 0b00000000) #QDCOUNT 0-7
	message = appendByteArray(message, 0b00000001) #QDCOUNT 8-15
	message = appendByteArray(message, 0b00000000) #ANCOUNT 0-7
	message = appendByteArray(message, 0b00000000) #ANCOUNT 8-15
	message = appendByteArray(message, 0b00000000) #NSCOUNT 0-7
	message = appendByteArray(message, 0b00000000) #NSCOUNT 8-15
	message = appendByteArray(message, 0b00000000) #ARCOUNT 0-7
	message = appendByteArray(message, 0b00000000) #ARCOUNT 8-15
	
	#Question section
	message = appendByteArray(message, 4) #QNAME length of www.google.com + null terminator
	message = appendByteArray(message, 'test')
	message = appendByteArray(message, 7)
	message = appendByteArray(message, 'iamotor')
	message = appendByteArray(message, 2)
	message = appendByteArray(message, 'nl')
	message = appendByteArray(message, 0b00000000) #QNAME: Null terminator
	message = appendByteArray(message, 0b00000000) #QTYPE: Octet 1
	message = appendByteArray(message, 0b00000001) #QTYPE: A Record
	message = appendByteArray(message, 0b00000000) #QCLASS byte 1: Internet
	message = appendByteArray(message, 0b00000001) #QCLASS byte 2: Internet
	return message

def sendUDPMessage(address, message):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(message, address)
	data = s.recv(512)
	s.close()
	return data