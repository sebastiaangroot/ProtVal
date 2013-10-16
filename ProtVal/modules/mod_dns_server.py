import modules.dnspacket
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
	packet = dnspacket.DNSPacket()
	packet.getStandardQueryPacket(domainname)
	response = sendMessage(packet.getPacketBytes(), address)
	p_response = packet.parseDNSPacket(response)

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