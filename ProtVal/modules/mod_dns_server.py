def verbosePrint(message, verbose, end='\n'):
	if not verbose:
		return
	print(message, end=end)

def testValue(num, expected, verbose):
	if num == expected:
		verbosePrint(' (OK)', verbose)
		return True
	else:
		verbosePrint(' (ERROR)', verbose)
		return False

def sendMessage(message, address):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(message, address)
	data = s.recv(4096)
	return data

def testStandardQuery(domainname, address, verbose):
	success = True
	p_query = getStandardQueryPacket()
	response = sendMessage(p_query, address)
	p_response = parseDNSPacket(response)
	
	verbosePrint(p_response.getPacketBytes(), verbose)

	#ID
	num = (p_response.header[0] << 8) + p_response.header[1]
	verbosePrint('Header ID: %i ' % num, verbose, end='')
	if not testValue(num, (p_query.header[0] << 8) + p_query.header[1], verbose):
		success = False
		
	#QR
	num = p_response.header[2] & 0b10000000
	verbosePrint('QR: %i ' % num, verbose, end='')
	if not testValue(num, 1, verbose):
		success = False
		
	#OPCODE
	num = p_response.header[2] & 0b01111000
	verbosePrint('OPCODE: %i ' % num, verbose, end='')
	if not testValue(num, 0, verbose):
		success = False

	#AA
	num = p_response.header[2] & 0b00000100
	verbosePrint('AA: %i ' % num, verbose, end='')
	if not testValue(num, 1, verbose):
		success = False

	#TC
	num = p_response.header[2] & 0b00000010
	verbosePrint('TC: %i' % num, verbose, end='')
	if not testValue(num, 0, verbose):
		success = False

	#RD
	num = p_response.header[2] & 0b00000001
	verbosePrint('RD: %i' % num, verbose, end='')
	if not testValue(num, 0, verbose):
		success = False

	#RA
	num = p_response.header[3] & 0b10000000
	verbosePrint('RA: %i' % num, verbose, end='')
	if not testValue(num, 1, verbose):
		success = False

	#Z
	num = p_response.header[3] & 0b01110000
	verbosePrint('Z: %i' % num, verbose, end='')
	if not testValue(num, 0, verbose):
		success = False

	#RCODE
	num = p_response.header[3] & 0b00001111
	verbosePrint('RCODE: %i' % num, verbose, end='')
	if not testValue(num, 0, verbose):
		success = False
	
	return success


def getModuleName():
	return "DNS Server Validator"

def getModuleDescription():
	return "A module to test your DNS server against the RFC"

def initMod():
	pass
