import dnspacket
import socket

def getModuleName():
	return "DNS Server Validator"

def getModuleDescription():
	return "A module to test your DNS server against the RFC"

def initMod():
	print('The following tests are available:')
	print('1. Standard Query validation')
	print('2. Inverse Query validation')
	print('3. Server status request availability test')
	print('4. Recursion availability test')
	print('5. QR bit error handling')
	print('6. OPCODE error handling')
	print('7. Z field error handling')
	print('8. Run all tests')
	choice = 0
	while True:
		answer = input('Please enter a test to run [1 - 8]: ')
		try:
			int(answer)
		except ValueError:
			continue
		else:
			choice = int(answer)
			if choice >= 1 or choice <= 8:
				break
			choice = 0
	
	if choice == 1:
		testStandardQuery('test.iamotor.nl', ('85.12.6.41', 53), True)
	elif choice == 2:
		testInverseQuery('85.12.6.41', ('85.12.6.41', 53), True)
	elif choice == 3:
		testServerStatusRequest(('85.12.6.41', 53), True)
	elif choice == 4:
		testRecursionAvailable('test.iamotor.nl', ('85.12.6.41', 53), True)
	elif choice == 5:
		testQRHandling('test.iamotor.nl', ('85.12.6.41', 53), True)
	elif choice == 6:
		testOPCODEHandling('test.iamotor.nl', ('85.12.6.41', 53), True)
	elif choice == 7:
		testZHandling('test.iamotor.nl', ('85.12.6.41', 53), True)
	elif choice == 8:
		result = testStandardQuery('test.iamotor.nl', ('85.12.6.41', 53), False)
		report('Standard Query:\t\t\t', result)

		result = testInverseQuery('85.12.6.41', ('85.12.6.41', 53), False)
		report('Inverse Query:\t\t\t', result)

		result = testServerStatusRequest(('85.12.6.41', 53), False)
		report('Server status request:\t', result)

		result = testRecursionAvailable('test.iamotor.nl', ('85.12.6.41', 53), False)
		report('Recursion available:\t\t', result)

		result = testQRHandling('test.iamotor.nl', ('85.12.6.41', 53), False)
		report('QR bit Error handling:\t', result)

		result = testOPCODEHandling('test.iamotor.nl', ('85.12.6.41', 53), False)
		report('OPCODE Error handling:\t', result)

		result = testZHandling('test.iamotor.nl', ('85.12.6.41', 53), False)
		report('Z Field error handling:\t', result)
				
def report(message, success):
	if success:
		print(message + '(OK)')
	else:
		print(message + '(ERROR)')

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
	aa = True
	packet = dnspacket.DNSPacket()
	packet.getStandardQueryPacket(domainname)
	response = sendMessage(packet.getPacketBytes(), address)
	p_response = packet.parseResponse(response)

	#ID
	num = int(p_response['ID'], 2)
	verbosePrint('Header ID: %s ' % p_response['ID'], verbose, end='')
	if not testValue(num, (packet.header[0] << 8) + packet.header[1], verbose):
		success = False
		
	#QR
	num = int(p_response['QR'], 2)
	verbosePrint('QR: %s ' % p_response['QR'], verbose, end='')
	if not testValue(num, 1, verbose):
		success = False
		
	#OPCODE
	num = int(p_response['OPCODE'], 2)
	verbosePrint('OPCODE: %s ' % p_response['OPCODE'], verbose, end='')
	if num == 0:
		verbosePrint(' (Standard Query)', verbose, end='')
	elif num == 1:
		verbosePrint(' (Inverse Query)', verbose, end='')
	elif num == 2:
		verbosePrint(' (Server Status Request)', verbose, end='')
	else:
		verbosePrint(' (Reserved)', verbose, end='')
	if not testValue(num, 0, verbose):
		success = False

	#AA
	num = int(p_response['AA'], 2)
	verbosePrint('AA: %s ' % p_response['AA'], verbose, end='\n')
	if not testValue(num, 1, False):
		aa = False

	#TC
	verbosePrint('TC: %s' % p_response['TC'], verbose, end='\n')

	#RD
	num = int(p_response['RD'], 2)
	verbosePrint('RD: %s' % p_response['RD'], verbose, end='')
	if not testValue(num, packet.header[2] & 0b00000001, verbose):
		success = False

	#RA
	verbosePrint('RA: %s' % p_response['RA'], verbose, end='\n')

	#Z
	num = int(p_response['Z'], 2)
	verbosePrint('Z: %s' % p_response['Z'], verbose, end='')
	if not testValue(num, 0, verbose):
		success = False

	#RCODE
	num = int(p_response['RCODE'], 2)
	verbosePrint('RCODE: %s' % p_response['RCODE'], verbose, end='')
	if num == 0:
		verbosePrint(' (No error)', verbose, end='')
	elif num == 1:
		verbosePrint(' (Format error)', verbose, end='')
	elif num == 2:
		verbosePrint(' (Server failure)', verbose, end='')
	elif num == 3:
		verbosePrint(' (Name error)', verbose, end='')
	elif num == 4:
		verbosePrint(' (Not implemented)', verbose, end='')
	elif num == 5:
		verbosePrint(' (Refused)', verbose, end='')
	else:
		verbosePrint(' (Unkown error)', verbose, end='')
	if not testValue(num, 0, verbose):
		success = False
	
	#QDCOUNT
	num = int(p_response['QDCOUNT'], 2)
	verbosePrint('QDCOUNT: %s' % p_response['QDCOUNT'], verbose, end='')
	if not testValue(num, (packet.header[4] << 8) + packet.header[5], verbose)
		success = False
	
	#ANCOUNT
	verbosePrint('ANCOUNT: %s' % p_response['ANCOUNT'], verbose, end='\n')

	#NSCOUNT
	verbosePrint('NSCOUNT: %s' % p_response['NSCOUNT'], verbose, end='\n')

	#ARCOUNT
	verbosePrint('ARCOUNT: %s' % p_response['ARCOUNT'], verbose, end='\n')

	
	return (success, p_response)