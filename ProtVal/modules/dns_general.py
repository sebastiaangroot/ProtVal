class DNSPacket():
	def __init__(self):
		self.header = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Enough room for the 12-byte header
		self.questions = []
		self.answers = []
		self.authorities = []
		self.additionals = []
	
	def __testValues__(self, num, min, max, functname):
		if num < min or num > max:
			raise ValueError('%s takes values from %i to %i' % (functname, min, max))
	
	def __testIndex__(self, list, index):
		if index >= 0 and len(list) < index + 1:
			return False
		if index < 0 and (0 - len(list)) < index:
			return False
		return True
	
	def __setHeaderValue__(self, num, min, max, functname, byte_i, mask, shift):
		self.__testValues__(num, min, max, functname)
		
		self.header[byte_i] = self.header[byte_i] & mask
		self.header[byte_i] += (num << shift)
	
	def __addRRNAME__(self, master_list, index, domainname):
		if type(master_list) != type(list):
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

	def __addRR32bit__(self, master_list, index, num):
		if type(master_list) != type(list):
			raise TypeError('__setRR32bit__ expected a list')
		if not self.__testIndex__(master_list, index):
			raise IndexError('__setRR32bit__ received an invalid list index')
		self.__testValues__(num, 0, 2**32 - 1, '__setRR32bit__')
		master_list[index] += num.to_bytes(4, 'big')
	
	def __addRR16bit__(self, master_list, index, num):
		if type(master_list) != type(list):
			raise TypeError('__setRR16bit__ expected a list')
		if not self.__testIndex__(master_list, index):
			raise IndexError('__setRR16bit__ received an invalid list index')
		self.__testValues__(num, 0, 2**16 - 1, '__setRR16bit__')
		master_list[index] += num.to_bytes(2, 'big')
	
	def __addRRRDATA__(self, master_list, index, data_list):
		if type(master_list) != type(list):
			raise TypeError('__addRRRDATA__ expected a list')
		if not self.__testIndex__(master_list, index):
			raise IndexError('__setRRRDATA__ received an invalid list index')
		if type(data_list) != type(list()):
			raise TypeError('__addRRRDATA__ expected a list for data_list')
		master_list[index] += data_list

	def getPacketBytes(self):
		return bytes(self.header)
	
	def createQuestionSection(self):
		self.questions.append([])

	def removeQuestionSection(self, question_i = -1):
		if len(self.questions) == 0:
			return
		if question_i == -1:
			question_i = len(self.questions) - 1
		del self.questions[question_i]

	def clearQuestion(self, question_i):
		if not self.__testIndex__(self.questions, question_i):
			return
		self.questions[question_i] = []
		
	def createAnswerSection(self):
		self.answers.append([])
	
	def removeAnswerSection(self, answer_i = -1):
		if len(self.answers) == 0:
			return
		if answer_i == -1:
			answer_i = len(self.answers) - 1
		del self.answers[answer_i]
		
	def createAuthoritySection(self):
		self.authorities.append([])
	
	def removeAuthoritySection(self, authority_i = -1):
		if len(self.authorities) == 0:
			return
		if authority_i == -1:
			authority_i = len(self.authorities) - 1
		del self.authorities[authority_i]
	
	def createAdditionalSection(self):
		self.additionals.append([])
		
	def removeAdditionalSection(self, additional_i = -1):
		if len(self.questions) == 0:
			return
		if additional_i == -1:
			additional_i = len(self.additionals) - 1
		del self.additionals[additional_i]
	
	def setHeaderID(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderID')
		
		bytes = num.to_bytes(2, 'big')
		self.header[0] = bytes[0]
		self.header[1] = bytes[1]
	
	def setHeaderQR(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderQR', 2, 0b01111111, 7)

	def setHeaderOPCODE(self, num):
		self.__setHeaderValue__(num, 0, 15, 'setHeaderOPCODE', 2, 0b10000111, 3)
	
	def setHeaderAA(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderAA', 2, 0b11111011, 2)
		
	def setHeaderTC(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderTC', 2, 0b11111101, 1)
	
	def setHeaderRD(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderRD', 2, 0b11111101, 0)
	
	def setHeaderRA(self, num):
		self.__setHeaderValue__(num, 0, 1, 'setHeaderRA', 3, 0b01111111, 7)
	
	def setHeaderZ(self, num):
		self.__setHeaderValue__(num, 0, 7, 'setHeaderZ', 3, 0b10001111, 4)
	
	def setHeaderRCODE(self, num):
		self.__setHeaderValue__(num, 0, 15, 'setHeaderRCODE', 3, 0b11110000, 0)
		
	def setHeaderQDCOUNT(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderQDCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.header[4] = bytes[0]
		self.header[5] = bytes[1]
	
	def setHeaderANCOUNT(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderANCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.header[6] = bytes[0]
		self.header[7] = bytes[1]
	
	def setHeaderNSCOUNT(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderNSCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.header[8] = bytes[0]
		self.header[9] = bytes[1]
	
	def setHeaderARCOUNT(self, num):
		self.__testValues__(num, 0, 2**16-1, 'setHeaderARCOUNT')
		
		bytes = num.to_bytes(2, 'big')
		self.header[10] = bytes[0]
		self.header[11] = bytes[1]
		
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
	
	def addQuestionQTYPE(self, num, question_i):
		if not self.__testIndex__(self.questions, question_i):
			return
		self.__testValues__(num, 0, 2**16-1, 'setQuestionQTYPE')
		self.questions[question_i] += num.to_bytes(2, 'big')

	def addQuestionQCLASS(self, num, question_i):
		if not self.__testIndex__(self.questions, question_i):
			return
		self.__testValues__(num, 0, 2**16-1, 'setQuestionQCLASS')
		self.questions[question_i] += num.to_bytes(2, 'big')
	
	def addAnswerNAME(self, domainname, index):
		self.__addRRNAME__(self.answers, index, domainname)
	
	def addAnswerTYPE(self, num, index):
		self.__addRR16bit__(self.answers, index, num)
	
	def addAnswerCLASS(self, num, index):
		self.__addRR16bit__(self.answers, index, num)
	
	def addAnswerTTL(self, num, index):
		self.__addRR32bit__(self.answers, index, num)
	
	def addAnswerRDLENGTH(self, num, index):
		self.__addRR16bit__(self.answers, index, num)
	
	def addAnswerRDATA(self, data_list, index):
		self.__addRRRDATA__(self.answers, index, data_list)
	
	def addAuthorityNAME(self, domainname, index):
		self.__addRRNAME__(self.authorities, index, domainname)
	
	def addAuthorityTYPE(self, num, index):
		self.__addRR16bit__(self.authorities, index, num)
	
	def addAuthorityCLASS(self, num, index):
		self.__addRR16bit__(self.authorities, index, num)
	
	def addAuthorityTTL(self, num, index):
		self.__addRR32bit__(self.answers, index, num)
	
	def addAuthorityRDLENGTH(self, num, index):
		self.__addRR16bit__(self.answers, index, num)
	
	def addAuthorityRDATA(self, num, data_list):
		self.__addRRRDATA__(self.answers, index, data_list)

	def addAdditionalNAME(self, domainname, index):
		self.__addRRNAME__(self.authorities, index, domainname)
	
	def addAdditionalTYPE(self, num, index):
		self.__addRR16bit__(self.authorities, index, num)
	
	def addAdditionalCLASS(self, num, index):
		self.__addRR16bit__(self.authorities, index, num)
	
	def addAdditionalTTL(self, num, index):
		self.__addRR32bit__(self.answers, index, num)
	
	def addAdditionalRDLENGTH(self, num, index):
		self.__addRR16bit__(self.answers, index, num)
	
	def addAdditionalRDATA(self, num, data_list):
		self.__addRRRDATA__(self.answers, index, data_list)