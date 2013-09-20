import math
import socket

class DNSPacket():
	def __init__(self):
		self.packet = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Enough room for the 12-byte header
	
	def __testValues__(self, num, min, max, functname):
		if num < min or num > max:
			raise ValueError('%s takes values from %i to %i' % (functname, min, max))
	
	def __setPacketValue__(self, num, min, max, functname, byte_i, mask, shift):
		__testValues__(num, min, max, functname)
		
		self.packet[byte_i] = self.packet[byte_i] & mask
		self.packet[byte_i] += (num << shift)
	
	def getPacketBytes(self):
		return bytes(self.packet)
	
	def setHeaderID(self, num):
		__testValues__(num, 0, 2**16-1, 'setHeaderID')
		
		bytes = num.to_bytes(2, 'big')
		self.packet[0] = bytes[0]
		self.packet[1] = bytes[1]
	
	def setHeaderQR(self, num):
		__setPacketValue__(num, 0, 1, 'setHeaderQR', 2, 0b01111111, 7)

	def setHeaderOPCODE(self, num):
		__setPacketValue__(num, 0, 15, 'setHeaderOPCODE', 2, 0b10000111, 3)
	
	def setHeaderAA(self, num):
		__setPacketValue__(num, 0, 1, 'setHeaderAA', 2, 0b11111011, 2)
		
	def setHeaderTC(self, num):
		__setPacketValue__(num, 0, 1, 'setHeaderTC', 2, 0b11111101, 1)
	
	def setHeaderRD(self, num):
		__setPacketValue__(num, 0, 1, 'setHeaderRD', 2, 0b11111101, 0)
	
	def setHeaderRA(self, num):
		__setPacketValue__(num, 0, 1, 'setHeaderRA', 3, 0b01111111, 7)
	
	def setHeaderZ(self, num):
		__setPacketValue__(num, 0, 7, 'setHeaderZ', 3, 0b10001111, 4)
	
	def setHeaderRCODE(self, num):
		__setPacketValue__(num, 0, 15, 'setHeaderRCODE', 3, 0b11110000, 0)
		
	def setHeaderQDCOUNT(self, num):
		__testValues__(num, 0, 2**16-1, 'setHeaderQDCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.packet[4] = bytes[0]
		self.packet[5] = bytes[1]
	
	def setHeaderANCOUNT(self, num):
		__testValues__(num, 0, 2**16-1, 'setHeaderANCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.packet[6] = bytes[0]
		self.packet[7] = bytes[1]
	
	def setHeaderNSCOUNT(self, num):
		__testValues__(num, 0, 2**16-1, 'setHeaderNSCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.packet[8] = bytes[0]
		self.packet[9] = bytes[1]
	
	def setHeaderARCOUNT(self, num):
		__testValues__(num, 0, 2**16-1, 'setHeaderARCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.packet[10] = bytes[0]
		self.packet[11] = bytes[1]
		
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