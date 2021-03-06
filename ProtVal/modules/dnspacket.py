#=====================================================================
#filename       : modules/dnspacket.py
#description    : DNS packet module for ProtVal
#python_version : 3.x
#=====================================================================

import socket
import random


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
	
	def removeBin(self, *value):
		"""
		This method receives a variable number of arguments and returns the correct binary representation. 
		If more then one argument is given, it will concatenate the binary representations.
		"""
		value_new = []
		for iterate in value:
			if len(iterate) > 2:
				iterate_stripped = iterate[2:]
				return_iterate = '0' * (8-len(iterate[2:])) + iterate_stripped
				value_new.append(return_iterate)
			elif len(iterate) <= 2:
				return_iterate = '0' * 8
				value_new.append('0' * 8)
			elif len(iterate) == 10:
				return_iterate = iterate[2:]
				value_new.append(return_iterate)
		value_return = ''
		for i in value_new:
			value_return += i
		return value_return
		
	
	def parseResponse(self, byte_array):
		"""
		This methods receives a byte array and parses them.
		The dict "reponse_items" holds all the values that are parsed.
		"""
		self.response_items['ID'] = self.removeBin(bin(byte_array[0]), bin(byte_array[1]))
		
		list_header = ['QR', 'OPCODE', 'AA', 'TC', 'RD'] #List that holds all the keywords that are used later in the program. 
		bin_header = self.removeBin(bin(byte_array[2])) #Example: Calling removeBin method and removes the 0b from the byte array.
		self.response_items[list_header[0]] = bin_header[0] #Example: add the returned value from removeBin with key/value pair QR="returned value"
		self.response_items[list_header[1]] = bin_header[1:5]
		i = 5
		while i < 8:
			self.response_items[list_header[i-3]] = bin_header[i]
			i += 1
		bin_header = self.removeBin(bin(byte_array[3]))
		self.response_items['RA'] = bin_header[0]
		self.response_items['Z'] = bin_header[1:4]
		self.response_items['RCODE'] = bin_header[4:]
		
		self.response_items['QDCOUNT'] = self.removeBin(bin(byte_array[4]), bin(byte_array[5]))
		self.response_items['ANCOUNT'] = self.removeBin(bin(byte_array[6]), bin(byte_array[7]))
		self.response_items['NSCOUNT'] = self.removeBin(bin(byte_array[8]), bin(byte_array[9]))
		self.response_items['ARCOUNT'] = self.removeBin(bin(byte_array[10]), bin(byte_array[11]))
		
		if len(byte_array) <= 12:
			return self.response_items
		"""
		Here comes the more complicated part. All byte_array values are iterated and checked if it's a label.
		"""
		iteration_read_label = 12 #Byte 12 always contains the first label.
		iteration_qdcount = int(self.removeBin(bin(byte_array[4]), bin(byte_array[5])), 2) #Same as QDCOUNT, this tells us how many question sections there are in this part.
		iteration_octet = byte_array[12] #This tells us how many characters we expect to parse (i.e. 4 for 'test').
		i = 0 #Just a variable that is used for counting an iteration. In this case it counts how many question sections we have parsed
		x = 0 #Just a variable that is used for counting an iteration. In this case it counts how many hostnames or subdomains we have parsed.
		y = 13 #Just a variable that is used for counting an iteration. In this case it counts which byte we have to parse for a specific character of a domain name (i.e. if it holds 15, and if the parser parses it we may get the value 't')
		z = 1 #Just a varaible that is used for counting an iteration. In this case it counts how many subdomains or hostnames we have parsed. (i.e. 1 could be test, 2 could be example, 3 could be .com)
		i_test = 0 #This variable is used as a boolean value. This checks if we have to add the QNAME/QTYPE/QCLASS section in the response_items dict.
		self.response_items
		self.temp_dict = {}
		while i < iteration_qdcount:
			if i_test == 0:
				self.response_items['QNAME'] = [[]] *iteration_qdcount #Adding the QNAME section as a list in a list. Multiple lists are created if the QDCOUNT variable is more than 1.
				self.response_items['QTYPE'] = [[]] *iteration_qdcount
				self.response_items['QCLASS'] = [[]] *iteration_qdcount
				i_test = 1
			while x < iteration_octet:
				self.temp_dict['domain_name_' + str(i) + str(z) +'part'] = self.temp_dict.setdefault('domain_name_' + str(i) + str(z) +'part', '') + chr(byte_array[y])
				x += 1
				y+=1
			self.response_items['QNAME'][i].append(self.temp_dict['domain_name_' + str(i) + str(z) +'part'])
			x = 0
			y += 1
			iteration_read_label += iteration_octet + 1
			iteration_octet = byte_array[iteration_read_label]
			z += 1
			if iteration_octet == 0:
				self.response_items['QTYPE'][i].append(self.removeBin(bin(byte_array[y]), bin(byte_array[y+1])))
				self.response_items['QCLASS'][i].append(self.removeBin(bin(byte_array[y+2]), bin(byte_array[y+3])))
				i += 1
				z = 1
				x = 0
				y += 4
				iteration_read_label = y
				try:
					iteration_octet = byte_array[iteration_read_label]
				except IndexError:
					return self.response_items
		iterable = y
		del self.temp_dict, iteration_read_label, iteration_qdcount, iteration_octet, i, x, y, z, i_test
		
		"""
		This is also a bit more complicated. Here we parse all ANCOUNT, NSCOUNT and ARCOUNT sections.
		"""
		
		ancount_entries = int(self.response_items['ANCOUNT'], 2) #Here we check how many ANCOUNT sections there are.
		nscount_entries = int(self.response_items['NSCOUNT'], 2)
		arcount_entries = int(self.response_items['ARCOUNT'], 2)
		entries = ancount_entries + nscount_entries + arcount_entries
		
		self.response_items['RR'] = []
		i = 0
		while i < entries:
			self.response_items['RR'].append({})
			i += 1
		
		i = 0
		name_start = iterable #We must know where to start. The variable "iterable" holds the value of the byte array that we must parse.
		reference = 0
		iteration_reference_loop = 0
		self.temp_dict = {}
		z= 0
		y = 0 #hoeveelste domeinnaam
		t = 0
		name_dict = str()
		name_count = 0
		iteration_reference = 0
		iter_loop = 0
		self.temp_dict_rdata = {}
		iteration_count = 0
		loop_count = 0
		
		
		while i < entries:
			if name_count < (entries - arcount_entries - nscount_entries):
				name_dict = 'ANCOUNT_ANSWER'
				
			elif name_count < (entries - arcount_entries):
				name_dict = 'NSCOUNT_ANSWER'
				
			elif name_count < (entries):
				name_dict = 'ARCOUNT_ANSWER'
			else:
				name_dict = 'ERROR'
			self.response_items['RR'][i]['NAME'] = list()
			if byte_array[name_start] & 0b11000000 == 0b11000000: #We must first check if the is a pointer, if this is the case we will start parsing. Note: this all happens in a while loop.
				while byte_array[name_start] & 0b11000000 == 0b11000000:
					reference = int(self.removeBin(bin(byte_array[name_start]), bin(byte_array[name_start+1]))[2:], 2)
					iteration_reference = byte_array[reference]
					iteration_count = reference + iteration_reference
					iter_loop = reference+1
					while True:
						while iteration_reference_loop < iteration_reference:					
							self.temp_dict['domain_name_' + str(t) + 'part'] = self.temp_dict.setdefault('domain_name_' + str(t) + 'part', '') + chr(byte_array[iter_loop])
							iter_loop += 1
							iteration_reference_loop += 1
		
						
						self.response_items['RR'][i]['NAME'].append(self.temp_dict['domain_name_' + str(t) + 'part'])
						
						iteration_reference_loop = 0
						iter_loop = iteration_count + 2
						t += 1
						iteration_reference = byte_array[iteration_count+1]
						iteration_count += 1
						iteration_count += iteration_reference
						if (iteration_reference == 0) | (iteration_reference == 192):
							
							if iteration_reference == 192:
								loop_count = byte_array[iteration_count-iteration_reference+1] #The RDATA section could also contain a pointer.
								iteration_reference = byte_array[loop_count]
								iter_loop = loop_count + 1
								iteration_count = iteration_reference + loop_count
								
								continue
							t=0
							name_start += 2
							break
					

					if byte_array[name_start] == 192:
						break

				
				

				
				self.response_items['RR'][i]['RR_TYPE'] = self.response_items['RR'][i].get('RR_TYPE', '') + name_dict
				
				

				self.response_items['RR'][i]['TYPE'] = self.response_items['RR'][i].get('TYPE', '') + self.removeBin(bin(byte_array[name_start]), bin(byte_array[name_start+1]))
				self.response_items['RR'][i]['CLASS'] = self.response_items['RR'][i].get('CLASS', '') + self.removeBin(bin(byte_array[name_start+2]), bin(byte_array[name_start+3]))
				self.response_items['RR'][i]['TTL'] = self.response_items['RR'][i].get('TTL', 0) + int(self.removeBin(bin(byte_array[name_start+4]), bin(byte_array[name_start+5]), bin(byte_array[name_start+6]), bin(byte_array[name_start+7])), 2)
				self.response_items['RR'][i]['RDLENGTH'] = self.response_items['RR'][i].get('RDLENGTH', 0) + int(self.removeBin(bin(byte_array[name_start+8]), bin(byte_array[name_start+9])),2)
				name_start += 10
				iter_loop_rdata = 0
				if byte_array[name_start] & 0b11000000 != 0b11000000:
					while iter_loop_rdata < self.response_items['RR'][i]['RDLENGTH']:
						self.temp_dict_rdata['RDATA'] = self.temp_dict_rdata.setdefault('RDATA', '') + str(byte_array[name_start])
						iter_loop_rdata += 1
						name_start += 1
					self.response_items['RR'][i]['RDATA'] = self.temp_dict_rdata['RDATA']
				else:
					self.response_items['RR'][i]['RDATA'] = int(self.removeBin(bin(byte_array[name_start]), bin(byte_array[name_start+1])))
					name_start += 2
				name_count += 1	
				i += 1
				self.temp_dict = {}
			else:
				raise Exception
		
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
	
	#Creates a inverse query, returns the DNSPacket object	
	def getInverseQueryPacket(self, domainname):
		self.setHeaderID(0b10011001)
		self.setHeaderQR(0)
		self.setHeaderOPCODE(1) # IQUERY
		self.setHeaderTC(0)
		self.setHeaderRD(1) # Query will be copied in the response
		self.setHeaderZ(0) # Must be zero in all queries and responses
		self.setHeaderQDCOUNT(1)
		i = self.createQuestionSection()
		self.addQuestionQNAME(domainname, i)
		self.addQuestionQTYPE(1, i)
		self.addQuestionQCLASS(1, i)
		
	#Creates a standard query with the QR bit set to 1, returns the DNSPacket object
	def getStandardQueryQRPacket(self, domainname):
		self.getStandardQueryPacket(domainname)
		self.setHeaderQR(1)

	#Creates a standard query with the OPCODE bits set to a value 3-15 at random, returns the DNSPacket object
	def getStandardQueryOPCODEPacket(self, domainname):
		opcode = random.randrange(3,5)
		self.getStandardQueryPacket(domainname)
		self.setHeaderOPCODE(opcode)

	#Creates a standard quer with the Z bits set to a value 1-7 at random, returns the DNSPacket object
	def getStandardQueryZPacket(self, domainname):
		zbits = random.randrange(1,7)
		self.getStandardQueryPacket(domainname)
		self.setHeaderZ(zbits)
	
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