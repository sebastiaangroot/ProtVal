import socket

class DNSPacket():
	def __init__(self):
		self.header = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Enough room for the 12-byte header
		self.questions = []
		self.answers = []
		self.authorities = []
		self.additionals = []
		self.answer_server = []
		self.response_items = {}
	
	#Raises a function-specific error if a given number is not between two limits
	def __testValues__(self, num, min, max, functname):
		if num < min or num > max:
			raise ValueError('%s takes values from %i to %i' % (functname, min, max))
	
	#Returns a boolean value depending on if given index exists in a list
	def __testIndex__(self, list, index):
		if index >= 0 and len(list) < index + 1:
			return False
		if index < 0 and (0 - len(list)) < index:
			return False
		return True
	
	#Clears existing bit field(s) in the header and replaces it with given num at offset byte_i + shift
	def __setHeaderValue__(self, num, min, max, functname, byte_i, mask, shift):
		self.__testValues__(num, min, max, functname)
		
		self.header[byte_i] = self.header[byte_i] & mask
		self.header[byte_i] += (num << shift)
	
	#Adds a domain name in the <domain-name> format (RFC 1035) to a given sublist
	def __addRRNAME__(self, master_list, index, domainname):
		if type(master_list) != type(list()):
			raise TypeError('__setRRName__ expected a list')
		if not self.__testIndex__(master_list, index):
			raise IndexError('__setRRName__ received an invalid list index')
		if type(domainname) != type(str()):
			raise TypeError('__setRRName__ expected a string')
		segments = domainname.split('.')
		for segment in segments:
			if len(segment) > 255:
				master_list[index].append(255)
			else:
				master_list[index].append(len(segment))
			master_list[index] += segment.encode()
		master_list[index].append(0)

	#Adds a 4-byte number to a given sublist
	def __addRR32bit__(self, master_list, index, num):
		if type(master_list) != type(list()):
			raise TypeError('__setRR32bit__ expected a list')
		if not self.__testIndex__(master_list, index):
			raise IndexError('__setRR32bit__ received an invalid list index')
		self.__testValues__(num, 0, 2**32 - 1, '__setRR32bit__')
		master_list[index] += num.to_bytes(4, 'big')
	
	#Adds a 2-byte number to a given sublist
	def __addRR16bit__(self, master_list, index, num):
		if type(master_list) != type(list()):
			raise TypeError('__setRR16bit__ expected a list')
		if not self.__testIndex__(master_list, index):
			raise IndexError('__setRR16bit__ received an invalid list index')
		self.__testValues__(num, 0, 2**16 - 1, '__setRR16bit__')
		master_list[index] += num.to_bytes(2, 'big')
	
	#Adds a list of arbitrary length to a given sublist
	def __addRRRDATA__(self, master_list, index, data_list):
		if type(master_list) != type(list()):
			raise TypeError('__addRRRDATA__ expected a list')
		if not self.__testIndex__(master_list, index):
			raise IndexError('__setRRRDATA__ received an invalid list index')
		if type(data_list) != type(list()):
			raise TypeError('__addRRRDATA__ expected a list for data_list')
		master_list[index] += data_list

	def bytestr(self, num):
		bin_num = bin(num)[2:]
		rest = 8 - len(bin_num)
		bin_num = ('0' * rest) + bin_num
		return bin_num
	
	def printHeader(self):
		print('+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
		print('|                      ID:%s                      |' % (self.bytestr(self.header[0]) + self.bytestr(self.header[1])))
		print('+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
		print('|QR%s|  OPCODE%s   |AA%s|TC%s|RD%s|RA%s|   Z%s    |   RCODE%s    |' % (self.bytestr(self.header[2])[0], self.bytestr(self.header[2])[1:5], self.bytestr(self.header[2])[5], self.bytestr(self.header[2])[6], self.bytestr(self.header[2])[7], self.bytestr(self.header[3])[0], self.bytestr(self.header[3])[1:4], self.bytestr(self.header[3])[4:7]))
		print('+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
		print('|                    QDCOUNT:%s                   |' % (self.bytestr(self.header[4]) + self.bytestr(self.header[5])))
		print('+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
		print('|                    ANCOUNT:%s                   |' % (self.bytestr(self.header[6]) + self.bytestr(self.header[7])))
		print('+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
		print('|                    NSCOUNT:%s                   |' % (self.bytestr(self.header[8]) + self.bytestr(self.header[9])))
		print('+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
		print('|                    ARCOUNT:%s                   |' % (self.bytestr(self.header[10]) + self.bytestr(self.header[11])))
		print('+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')

	#Returns a byte array of the packet, for sending it over a socket
	def getPacketBytes(self):
		packet = bytes(self.header)
		for question in self.questions:
			packet = packet + bytes(question)
		for answer in self.answers:
			packet = packet + bytes(answer)
		for authority in self.authorities:
			packet = packet + bytes(authority)
		for additional in self.additionals:
			packet = packet + bytes(additional)
		return packet
	
	def removeBin(self, value):
		if len(value) > 2:
			value_stripped = value[2:]
			return_value = '0' * (8-len(value[2:])) + value_stripped
			print('debug', return_value)
			return return_value
		elif len(value) <= 2:
			return_value = '0' * 8
			print('debug', return_value)
			return '0' * 8
		elif len(value) == 10:
			return_value = value[2:]
			print('debug', return_value)
			return return_value
		
	
	def parseResponse(self, byte_array):
		
		print("Inside parseResponse") #for debugging purposes
		print("Printing byte_array:", byte_array)
		#print("test:", byte_array[1])
		self.response_items['ID'] = self.removeBin(bin(byte_array[0] +byte_array[1]))
		#print(self.response_items['ID'])
		#print('test byte_array', bin(byte_array[1]))
		
		list_header = ['QR', 'OPCODE', 'AA', 'TC', 'RD']
		bin_header = self.removeBin(bin(byte_array[2]))
		#print(bin_header)
		self.response_items[list_header[0]] = bin_header[0]
		self.response_items[list_header[1]] = bin_header[1:5]
		i = 5
		while i < 8:
			self.response_items[list_header[i-3]] = bin_header[i]
			i += 1
		bin_header = self.removeBin(bin(byte_array[3]))
		#print('bin_header', bin_header)
		#print('testen', byte_array[3])
		self.response_items['RA'] = bin_header[0]
		self.response_items['Z'] = bin_header[1:4]
		self.response_items['RCODE'] = bin_header[4:]
		
		self.response_items['QDCOUNT'] = self.removeBin(bin(byte_array[4] +byte_array[5]))
		self.response_items['ANCOUNT'] = self.removeBin(bin(byte_array[6] +byte_array[7]))
		self.response_items['NSCOUNT'] = self.removeBin(bin(byte_array[8] +byte_array[9]))
		self.response_items['ARCOUNT'] = self.removeBin(bin(byte_array[10] +byte_array[11]))
		
		iteration_read_label = 12
		iteration_qdcount = byte_array[4] +byte_array[5]
		iteration_octet = byte_array[12]
		i = 0
		x = 0
		y = 13
		z = 1
		i_test = 0
		self.response_items
		self.temp_dict = {}
		while i < iteration_qdcount:
			if i_test == 0 and iteration_qdcount == 1:
				self.response_items['QNAME'] = []
				#print ('test') 
				i_test = 1
			elif i_test == 0:
				self.response_items['QNAME'] = [[]] *iteration_qdcount
				i_test = 1
			while x < iteration_octet:
				#print('inside x<iteration_octet')
				self.temp_dict['domain_name_' + str(i) + str(z) +'part'] = self.temp_dict.setdefault('domain_name_' + str(i) + str(z) +'part', '') + chr(byte_array[y])
				#print(chr(byte_array[y]))
				x += 1
				y+=1
			if iteration_qdcount ==1:
				self.response_items['QNAME'].append(self.temp_dict['domain_name_' + str(i) + str(z) +'part'])
			else:
				self.response_items['QNAME'][i].append(self.temp_dict['domain_name_' + str(i) + str(z) +'part'])
			x = 0
			y += 1
			#print('x is:', x, 'y is:', y, 'z is:', z)
			iteration_read_label += iteration_octet + 1
			iteration_octet = byte_array[iteration_read_label]
			z += 1
			if iteration_octet == 0:
				i += 1
				z = 1
				x = 0
				y = iteration_read_label + 2
				iteration_read_label += 2
				iteration_octet = byte_array[iteration_read_label]
				print('y is:', y)
		del self.temp_dict
		iterable = y
		
		print('iterable:', iterable)
		
		print(self.response_items)
		return(self.response_items)
		
	def testResponse(self):
		buffer_size = 1024
		
		
		self.setHeaderID(0b10011001)
		self.setHeaderRD(1)
		self.setHeaderQDCOUNT(1)
		i = self.createQuestionSection()
		self.addQuestionQNAME('test.iamotor.nl', i)
		self.addQuestionQTYPE(1, i)
		self.addQuestionQCLASS(1, i)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.sendto(self.getPacketBytes(), ('85.12.6.41', 53))
		self.data = s.recv(buffer_size)
		s.close()
		return self.data
		
	#Creates a standard query, returns the DNSPacket object
	def getStandardQueryPacket(self, domainname):
		buffer_size = 1024
		
		self.setHeaderID(0b10011001)
		self.setHeaderQR(0)
		self.setHeaderOPCODE(0)
		self.setHeaderTC(0) #Set to not-truncated for now
		self.setHeaderRD(1) #Query will be copied in the response
		self.setHeaderZ(0) #Must be zero in all queries and responses
		self.setHeaderQDCOUNT(1)
		i = self.createQuestionSection()
		self.addQuestionQNAME(domainname, i)
		self.addQuestionQTYPE(1, i) #A, IPv4 address
		self.addQuestionQCLASS(1, i)
	
	#Creates a new question section in the self.questions master list
	def createQuestionSection(self):
		self.questions.append([])
		return len(self.questions) - 1

	#Removes a given (or the last) question section of the self.questions master list
	def removeQuestionSection(self, question_i = -1):
		if len(self.questions) == 0:
			return
		if question_i == -1:
			question_i = len(self.questions) - 1
		del self.questions[question_i]

	#Keeps the given question section, but clears it of data
	def clearQuestionSection(self, question_i):
		if not self.__testIndex__(self.questions, question_i):
			return
		self.questions[question_i] = []
		
	def createAnswerSection(self):
		self.answers.append([])
		return len(self.answers) - 1
	
	def removeAnswerSection(self, answer_i = -1):
		if len(self.answers) == 0:
			return
		if answer_i == -1:
			answer_i = len(self.answers) - 1
		del self.answers[answer_i]
		
	def clearAnswerSection(self, answer_i):
		if not self.__testIndex__(self.answers, answer_i):
			return
		self.answers[answer_i] = []

	def createAuthoritySection(self):
		self.authorities.append([])
		return len(self.authorities) - 1
	
	def removeAuthoritySection(self, authority_i = -1):
		if len(self.authorities) == 0:
			return
		if authority_i == -1:
			authority_i = len(self.authorities) - 1
		del self.authorities[authority_i]

	def clearAuthoritySection(self, authority_i):
		if not self.__testIndex__(self.authorities, authority_i):
			return
		self.authorities[authority_i] = []

	def createAdditionalSection(self):
		self.additionals.append([])
		return len(self.additionals) - 1
		
	def removeAdditionalSection(self, additional_i = -1):
		if len(self.questions) == 0:
			return
		if additional_i == -1:
			additional_i = len(self.additionals) - 1
		del self.additionals[additional_i]
	
	def clearAdditionalSection(self, additional_i):
		if not self.__testIndex__(self.additionals, additional_i):
			return
		self.additionals[additional_i] = []

	#Sets the two ID bytes of the DNS header
	def setHeaderID(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderID')
		
		bytes = num.to_bytes(2, 'big')
		self.header[0] = bytes[0]
		self.header[1] = bytes[1]

	#Sets the QR bit of the DNS header
	def setHeaderQR(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderQR', 2, 0b01111111, 7)

	#Sets the four OPCODE bits of the DNS header
	def setHeaderOPCODE(self, num):
		self.__setHeaderValue__(num, 0, 15, 'setHeaderOPCODE', 2, 0b10000111, 3)

	#Sets the AA bit of the DNS header
	def setHeaderAA(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderAA', 2, 0b11111011, 2)

	#Sets the TC bit of the DNS header
	def setHeaderTC(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderTC', 2, 0b11111101, 1)

	#Sets the RD bit of the DNS header
	def setHeaderRD(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderRD', 2, 0b11111101, 0)

	#Sets the RA bit of the DNS header
	def setHeaderRA(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderRA', 3, 0b01111111, 7)

	#Sets the three Z bits of the DNS header
	def setHeaderZ(self, num):
		self.__setHeaderValue__(num, 0, 7, 'setHeaderZ', 3, 0b10001111, 4)

	#Sets the four RCODE  bits of the DNS header
	def setHeaderRCODE(self, num):
		self.__setHeaderValue__(num, 0, 15, 'setHeaderRCODE', 3, 0b11110000, 0)

	#Sets the two QDCOUNT bytes of the DNS header
	def setHeaderQDCOUNT(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderQDCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.header[4] = bytes[0]
		self.header[5] = bytes[1]

	#Sets the two ANCOUNT bytes of the DNS header
	def setHeaderANCOUNT(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderANCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.header[6] = bytes[0]
		self.header[7] = bytes[1]

	#Sets the two NSCOUNT bytes of the DNS header
	def setHeaderNSCOUNT(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderNSCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.header[8] = bytes[0]
		self.header[9] = bytes[1]

	#Sets the two ARCOUNT bytes of the DNS header
	def setHeaderARCOUNT(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderARCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.header[10] = bytes[0]
		self.header[11] = bytes[1]

	#Adds a QNAME field to a given question section
	def addQuestionQNAME(self, domainname, question_i):
		if not self.__testIndex__(self.questions, question_i):
			return
		segments = domainname.split('.')
		for segment in segments:
			if len(segment) > 255:
				self.questions[question_i].append(255)
			else:
				self.questions[question_i].append(len(segment))
			self.questions[question_i] += segment.encode()
		self.questions[question_i].append(0)

	#Adds a QTYPE field to a given question section
	def addQuestionQTYPE(self, num, question_i):
		if not self.__testIndex__(self.questions, question_i):
			return
		self.__testValues__(num, 0, 2**16-1, 'setQuestionQTYPE')
		self.questions[question_i] += num.to_bytes(2, 'big')

	#Adds a QCLASS field to a given question section
	def addQuestionQCLASS(self, num, question_i):
		if not self.__testIndex__(self.questions, question_i):
			return
		self.__testValues__(num, 0, 2**16-1, 'setQuestionQCLASS')
		self.questions[question_i] += num.to_bytes(2, 'big')

	#Adds a Resource Record NAME field to a given answer section
	def addAnswerNAME(self, domainname, index):
		self.__addRRNAME__(self.answers, index, domainname)

	#Adds a Resource Record TYPE field to a given answer section
	def addAnswerTYPE(self, num, index):
		self.__addRR16bit__(self.answers, index, num)

	#Adds a Resource Record CLASS field to a given answer section
	def addAnswerCLASS(self, num, index):
		self.__addRR16bit__(self.answers, index, num)

	#Adds a Resource Record TTL field to a given answer section
	def addAnswerTTL(self, num, index):
		self.__addRR32bit__(self.answers, index, num)

	#Adds a Resource Record RDLENGTH field to a given answer section
	def addAnswerRDLENGTH(self, num, index):
		self.__addRR16bit__(self.answers, index, num)

	#Adds a Resource Record RDATA field to a given answer section given a data list of arbitrary length
	def addAnswerRDATA(self, data_list, index):
		self.__addRRRDATA__(self.answers, index, data_list)
	
	def addAuthorityNAME(self, domainname, index):
		self.__addRRNAME__(self.authorities, index, domainname)
	
	def addAuthorityTYPE(self, num, index):
		self.__addRR16bit__(self.authorities, index, num)
	
	def addAuthorityCLASS(self, num, index):
		self.__addRR16bit__(self.authorities, index, num)
	
	def addAuthorityTTL(self, num, index):
		self.__addRR32bit__(self.authorities, index, num)
	
	def addAuthorityRDLENGTH(self, num, index):
		self.__addRR16bit__(self.authorities, index, num)
	
	def addAuthorityRDATA(self, num, data_list):
		self.__addRRRDATA__(self.authorities, index, data_list)

	def addAdditionalNAME(self, domainname, index):
		self.__addRRNAME__(self.additionals, index, domainname)
	
	def addAdditionalTYPE(self, num, index):
		self.__addRR16bit__(self.additionals, index, num)
	
	def addAdditionalCLASS(self, num, index):
		self.__addRR16bit__(self.additionals, index, num)
	
	def addAdditionalTTL(self, num, index):
		self.__addRR32bit__(self.additionals, index, num)
	
	def addAdditionalRDLENGTH(self, num, index):
		self.__addRR16bit__(self.additionals, index, num)
	
	def addAdditionalRDATA(self, num, data_list):
		self.__addRRRDATA__(self.additionals, index, data_list)

def main():
	print("Class methods names of DNSPacket")
	for i in dir(DNSPacket):
		if '_' not in i:
			print(i)
	q = DNSPacket()
	byte_array = q.testResponse()
	q.parseResponse(byte_array)
	
# 	print('Koen\'s test')
# 	r = DNSPacket()
# 	standard_array = r.getStandardQueryPacket('koenveelenturf.nl')
# 	print('standard_array:', standard_array)
# 	print(r.header)
# 	print(r.questions)	
# 	print(r.parseResponse(standard_array))
		
if __name__ == '__main__':
	main()
