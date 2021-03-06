#=====================================================================
#filename       : modules/mod_dns_server.py
#description    : DNS server module for ProtVal
#python_version : 3.x
#=====================================================================

import modules.dnspacket as dnspacket
import socket
import traceback

def getModuleName():
	return "DNS Server Validator"

def getModuleDescription():
	return "A module to test your DNS server against the RFC"

def initMod():
	while True:
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
			dn = input('Enter a domainname to query: ')
			dest_ip = input('Enter the IP address of the DNS server: ')
			dest_port = input('Enter the port to contact the DNS server on (53 is default): ')
			if dest_port == '':
				dest_port = 53
			try:
				result = testStandardQuery(dn, (dest_ip, int(dest_port)), True)
				report('\nStandard Query:\t\t\t', result)
			except:
				print('Error while calling testStandardQuery')
				traceback.print_exc()
		elif choice == 2:
			q_ip = input('Enter an IP address to inverse query: ')
			dest_ip = input('Enter the IP address of the DNS server: ')
			dest_port = input('Enter the port to contact the DNS server on (53 is default): ')
			if dest_port == '':
				dest_port = 53
			try:
				result = testInverseQuery(q_ip, (dest_ip, int(dest_port)), True)
				report('\nInverse Query:\t\t\t', result)
			except:
				print('Error while calling testInverseQuery')
				traceback.print_exc()
		elif choice == 3:
			dest_ip = input('Enter the IP address of the DNS server: ')
			dest_port = input('Enter the port to contact the DNS server on (53 is default): ')
			if dest_port == '':
				dest_port = 53
			try:
				result = testServerStatusRequest((dest_ip, int(dest_port)), True)
				report('\nServer status request:\t', result)
			except:
				print('Error while calling testServerStatusRequest')
				traceback.print_exc()
		elif choice == 4:
			dn = input('Enter a domainname to query: ')
			dest_ip = input('Enter the IP address of the DNS server: ')
			dest_port = input('Enter the port to contact the DNS server on (53 is default): ')
			if dest_port == '':
				dest_port = 53
			try:
				result = testRecursionAvailable(dn, (dest_ip, int(dest_port)), True)
				report('\nRecursion available:\t\t', result)
			except:
				print('Error while calling testRecursionAvailable')
				traceback.print_exc()
		elif choice == 5:
			dn = input('Enter a domainname to query: ')
			dest_ip = input('Enter the IP address of the DNS server: ')
			dest_port = input('Enter the port to contact the DNS server on (53 is default): ')
			if dest_port == '':
				dest_port = 53
			try:
				result = testQRHandling(dn, (dest_ip, int(dest_port)), True)
				report('\nQR bit Error handling:\t', result)
			except:
				print('Error while calling testQRHandling')
				traceback.print_exc()
		elif choice == 6:
			dn = input('Enter a domainname to query: ')
			dest_ip = input('Enter the IP address of the DNS server: ')
			dest_port = input('Enter the port to contact the DNS server on (53 is default): ')
			if dest_port == '':
				dest_port = 53
			try:
				result = testOPCODEHandling(dn, (dest_ip, int(dest_port)), True)
				report('\nOPCODE Error handling:\t', result)
			except:
				print('Error while calling testOPCODEHandling')
				traceback.print_exc()
		elif choice == 7:
			dn = input('Enter a domainname to query: ')
			dest_ip = input('Enter the IP address of the DNS server: ')
			dest_port = input('Enter the port to contact the DNS server on (53 is default): ')
			if dest_port == '':
				dest_port = 53
			try:
				result = testZHandling(dn, (dest_ip, int(dest_port)), True)
				report('\nZ Field error handling:\t', result)
			except:
				print('Error while calling testZHandling')
				traceback.print_exc()
		elif choice == 8:
			dn = input('Enter a domainname to query: ')
			q_ip = input('Enter an IP address to inverse query: ')
			dest_ip = input('Enter the IP address of the DNS server: ')
			dest_port = input('Enter the port to contact the DNS server on (53 is default): ')
			if dest_port == '':
				dest_port = 53
			try:
				result = testStandardQuery(dn, (dest_ip, int(dest_port)), False)
				report('Standard Query:\t\t\t', result)
			except:
				print('Error while calling testStandardQuery')
				traceback.print_exc()

			try:
				result = testInverseQuery(q_ip, (dest_ip, int(dest_port)), False)
				report('Inverse Query:\t\t\t', result)
			except:
				print('Error while calling testInverseQuery')
				traceback.print_exc()

			try:
				result = testServerStatusRequest((dest_ip, int(dest_port)), False)
				report('Server status request:\t', result)
			except:
				print('Error while calling testServerStatusRequest')
				traceback.print_exc()

			try:
				result = testRecursionAvailable(dn, (dest_ip, int(dest_port)), False)
				report('Recursion available:\t\t', result)
			except:
				print('Error while calling testRecursionAvailable')
				traceback.print_exc()

			try:
				result = testQRHandling(dn, (dest_ip, int(dest_port)), False)
				report('QR bit Error handling:\t', result)
			except:
				print('Error while calling testQRHandling')
				traceback.print_exc()

			try:
				result = testOPCODEHandling(dn, (dest_ip, int(dest_port)), False)
				report('OPCODE Error handling:\t', result)
			except:
				print('Error while calling testOPCODEHandling')
				traceback.print_exc()

			try:
				result = testZHandling(dn, (dest_ip, int(dest_port)), False)
				report('Z Field error handling:\t', result)
			except:
				print('Error while calling testZHandling')
				traceback.print_exc()
				
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
	s.settimeout(1)
	s.sendto(message, address)
	try:
		data = s.recv(4096)
	except socket.timeout:
		return None
	return data

def testStandardQuery(domainname, address, verbose):
	success = True
	aa = True
	packet = dnspacket.DNSPacket()
	packet.getStandardQueryPacket(domainname)
	response = sendMessage(packet.getPacketBytes(), address)
	if response == None:
		verbosePrint('No response was received', verbose)
		return False
	p_response = packet.parseResponse(response)

	verbosePrint('############################################\nHeader:', verbose)
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
	if not testValue(num, (packet.header[4] << 8) + packet.header[5], verbose):
		success = False
	
	#ANCOUNT
	verbosePrint('ANCOUNT: %s' % p_response['ANCOUNT'], verbose, end='\n')

	#NSCOUNT
	verbosePrint('NSCOUNT: %s' % p_response['NSCOUNT'], verbose, end='\n')

	#ARCOUNT
	verbosePrint('ARCOUNT: %s' % p_response['ARCOUNT'], verbose, end='\n')

	for i in range(0, int(p_response['QDCOUNT'], 2)):
		verbosePrint('############################################\nQuestion section %i' % i, verbose)
		verbosePrint('QNAME: ', verbose, end='')
		for j, label in enumerate(p_response['QNAME'][i]):
			verbosePrint(label, verbose, end='')
			if j < len(p_response['QNAME'][i]) - 1:
				verbosePrint('.', verbose, end='')
			else:
				verbosePrint('', verbose)
		verbosePrint('QCLASS: %s' % p_response['QCLASS'][i][0], verbose)
		verbosePrint('QTYPE: %s' % p_response['QTYPE'][i][0], verbose)
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ANCOUNT_ANSWER':
				verbosePrint('############################################\nAnswer section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'NSCOUNT_ANSWER':
				verbosePrint('############################################\nAuthority section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ARCOUNT_ANSWER':
				verbosePrint('############################################\nAdditional section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	return success

def testInverseQuery(ip, address, verbose):
	success = True
	aa = True
	packet = dnspacket.DNSPacket()
	packet.getInverseQueryPacket(ip)
	response = sendMessage(packet.getPacketBytes(), address)
	if response == None:
		verbosePrint('No response was received', verbose)
		return False
	p_response = packet.parseResponse(response)

	verbosePrint('############################################\nHeader:', verbose)
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
	if not testValue(num, 1, verbose):
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
	if not testValue(num, (packet.header[4] << 8) + packet.header[5], verbose):
		success = False
	
	#ANCOUNT
	verbosePrint('ANCOUNT: %s' % p_response['ANCOUNT'], verbose, end='\n')

	#NSCOUNT
	verbosePrint('NSCOUNT: %s' % p_response['NSCOUNT'], verbose, end='\n')

	#ARCOUNT
	verbosePrint('ARCOUNT: %s' % p_response['ARCOUNT'], verbose, end='\n')

	for i in range(0, int(p_response['QDCOUNT'], 2)):
		verbosePrint('############################################\nQuestion section %i' % i, verbose)
		verbosePrint('QNAME: ', verbose, end='')
		for j, label in enumerate(p_response['QNAME'][i]):
			verbosePrint(label, verbose, end='')
			if j < len(p_response['QNAME'][i]) - 1:
				verbosePrint('.', verbose, end='')
			else:
				verbosePrint('', verbose)
		verbosePrint('QCLASS: %s' % p_response['QCLASS'][i][0], verbose)
		verbosePrint('QTYPE: %s' % p_response['QTYPE'][i][0], verbose)
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ANCOUNT_ANSWER':
				verbosePrint('############################################\nAnswer section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'NSCOUNT_ANSWER':
				verbosePrint('############################################\nAuthority section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ARCOUNT_ANSWER':
				verbosePrint('############################################\nAdditional section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	return success

def testServerStatusRequest(address, verbose):
	success = True
	aa = True
	packet = dnspacket.DNSPacket()
	packet.setHeaderID(0b10011001)
	packet.setHeaderQR(0)
	packet.setHeaderOPCODE(2) #Server status request
	packet.setHeaderTC(0)
	packet.setHeaderRD(0)
	packet.setHeaderZ(0)


	response = sendMessage(packet.getPacketBytes(), address)
	if response == None:
		verbosePrint('No response was received', verbose)
		return False
	p_response = packet.parseResponse(response)

	verbosePrint('############################################\nHeader:', verbose)
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
	if not (testValue(num, 0, verbose) or testValue(num, 4, verbose)):
		success = False
	
	#QDCOUNT
	num = int(p_response['QDCOUNT'], 2)
	verbosePrint('QDCOUNT: %s' % p_response['QDCOUNT'], verbose, end='')
	if not testValue(num, (packet.header[4] << 8) + packet.header[5], verbose):
		success = False
	
	#ANCOUNT
	verbosePrint('ANCOUNT: %s' % p_response['ANCOUNT'], verbose, end='\n')

	#NSCOUNT
	verbosePrint('NSCOUNT: %s' % p_response['NSCOUNT'], verbose, end='\n')

	#ARCOUNT
	verbosePrint('ARCOUNT: %s' % p_response['ARCOUNT'], verbose, end='\n')

	for i in range(0, int(p_response['QDCOUNT'], 2)):
		verbosePrint('############################################\nQuestion section %i' % i, verbose)
		verbosePrint('QNAME: ', verbose, end='')
		for j, label in enumerate(p_response['QNAME'][i]):
			verbosePrint(label, verbose, end='')
			if j < len(p_response['QNAME'][i]) - 1:
				verbosePrint('.', verbose, end='')
			else:
				verbosePrint('', verbose)
		verbosePrint('QCLASS: %s' % p_response['QCLASS'][i][0], verbose)
		verbosePrint('QTYPE: %s' % p_response['QTYPE'][i][0], verbose)
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ANCOUNT_ANSWER':
				verbosePrint('############################################\nAnswer section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'NSCOUNT_ANSWER':
				verbosePrint('############################################\nAuthority section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ARCOUNT_ANSWER':
				verbosePrint('############################################\nAdditional section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	return success

def testRecursionAvailable(domainname, address, verbose):
	success = True
	packet = dnspacket.DNSPacket()
	packet.getStandardQueryPacket(domainname)
	response = sendMessage(packet.getPacketBytes(), address)
	if response == None:
		verbosePrint('No response was received', verbose)
		return False
	p_response = packet.parseResponse(response)

	verbosePrint('############################################\nHeader:', verbose)
	#ID
	num = int(p_response['ID'], 2)
	verbosePrint('Header ID: %s ' % p_response['ID'], verbose)
		
	#QR
	num = int(p_response['QR'], 2)
	verbosePrint('QR: %s ' % p_response['QR'], verbose)
		
	#OPCODE
	num = int(p_response['OPCODE'], 2)
	verbosePrint('OPCODE: %s ' % p_response['OPCODE'], verbose)
	if num == 0:
		verbosePrint(' (Standard Query)', verbose)
	elif num == 1:
		verbosePrint(' (Inverse Query)', verbose)
	elif num == 2:
		verbosePrint(' (Server Status Request)', verbose)
	else:
		verbosePrint(' (Reserved)', verbose)

	#AA
	num = int(p_response['AA'], 2)
	verbosePrint('AA: %s ' % p_response['AA'], verbose)

	#TC
	verbosePrint('TC: %s' % p_response['TC'], verbose)

	#RD
	num = int(p_response['RD'], 2)
	verbosePrint('RD: %s' % p_response['RD'], verbose, end='')
	if not testValue(num, packet.header[2] & 0b00000001, verbose):
		success = False

	#RA
	num = int(p_response['RA'], 2)
	verbosePrint('RA: %s' % p_response['RA'], verbose, end='')
	if not testValue(num, packet.header[3] & 0b10000000, verbose):
		success = False

	#Z
	num = int(p_response['Z'], 2)
	verbosePrint('Z: %s' % p_response['Z'], verbose, end='')

	#RCODE
	num = int(p_response['RCODE'], 2)
	verbosePrint('RCODE: %s' % p_response['RCODE'], verbose, end='')
	if num == 0:
		verbosePrint(' (No error)', verbose)
	elif num == 1:
		verbosePrint(' (Format error)', verbose)
	elif num == 2:
		verbosePrint(' (Server failure)', verbose)
	elif num == 3:
		verbosePrint(' (Name error)', verbose)
	elif num == 4:
		verbosePrint(' (Not implemented)', verbose)
	elif num == 5:
		verbosePrint(' (Refused)', verbose)
	else:
		verbosePrint(' (Unkown error)', verbose)
	
	#QDCOUNT
	num = int(p_response['QDCOUNT'], 2)
	verbosePrint('QDCOUNT: %s' % p_response['QDCOUNT'], verbose)
	
	#ANCOUNT
	verbosePrint('ANCOUNT: %s' % p_response['ANCOUNT'], verbose)

	#NSCOUNT
	verbosePrint('NSCOUNT: %s' % p_response['NSCOUNT'], verbose)

	#ARCOUNT
	verbosePrint('ARCOUNT: %s' % p_response['ARCOUNT'], verbose)

	for i in range(0, int(p_response['QDCOUNT'], 2)):
		verbosePrint('############################################\nQuestion section %i' % i, verbose)
		verbosePrint('QNAME: ', verbose, end='')
		for j, label in enumerate(p_response['QNAME'][i]):
			verbosePrint(label, verbose, end='')
			if j < len(p_response['QNAME'][i]) - 1:
				verbosePrint('.', verbose, end='')
			else:
				verbosePrint('', verbose)
		verbosePrint('QCLASS: %s' % p_response['QCLASS'][i][0], verbose)
		verbosePrint('QTYPE: %s' % p_response['QTYPE'][i][0], verbose)
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ANCOUNT_ANSWER':
				verbosePrint('############################################\nAnswer section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'NSCOUNT_ANSWER':
				verbosePrint('############################################\nAuthority section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ARCOUNT_ANSWER':
				verbosePrint('############################################\nAdditional section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	return success

def testQRHandling(domainname, address, verbose):
	success = True
	packet = dnspacket.DNSPacket()
	packet.getStandardQueryQRPacket(domainname)
	response = sendMessage(packet.getPacketBytes(), address)
	if response == None:
		verbosePrint('No response was received', verbose)
		return False
	p_response = packet.parseResponse(response)

	verbosePrint('############################################\nHeader:', verbose)
	#ID
	num = int(p_response['ID'], 2)
	verbosePrint('Header ID: %s ' % p_response['ID'], verbose)
		
	#QR
	num = int(p_response['QR'], 2)
	verbosePrint('QR: %s ' % p_response['QR'], verbose)
		
	#OPCODE
	num = int(p_response['OPCODE'], 2)
	verbosePrint('OPCODE: %s ' % p_response['OPCODE'], verbose, end='')
	if num == 0:
		verbosePrint(' (Standard Query)', verbose)
	elif num == 1:
		verbosePrint(' (Inverse Query)', verbose)
	elif num == 2:
		verbosePrint(' (Server Status Request)', verbose)
	else:
		verbosePrint(' (Reserved)', verbose)

	#AA
	verbosePrint('AA: %s ' % p_response['AA'], verbose)

	#TC
	verbosePrint('TC: %s' % p_response['TC'], verbose)

	#RD
	verbosePrint('RD: %s' % p_response['RD'], verbose)

	#RA
	verbosePrint('RA: %s' % p_response['RA'], verbose)

	#Z
	verbosePrint('Z: %s' % p_response['Z'], verbose)

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
	if not testValue(num, 1, verbose):
		success = False
	
	#QDCOUNT
	verbosePrint('QDCOUNT: %s' % p_response['QDCOUNT'], verbose)
	
	#ANCOUNT
	verbosePrint('ANCOUNT: %s' % p_response['ANCOUNT'], verbose)

	#NSCOUNT
	verbosePrint('NSCOUNT: %s' % p_response['NSCOUNT'], verbose)

	#ARCOUNT
	verbosePrint('ARCOUNT: %s' % p_response['ARCOUNT'], verbose)

	for i in range(0, int(p_response['QDCOUNT'], 2)):
		verbosePrint('############################################\nQuestion section %i' % i, verbose)
		verbosePrint('QNAME: ', verbose, end='')
		for j, label in enumerate(p_response['QNAME'][i]):
			verbosePrint(label, verbose, end='')
			if j < len(p_response['QNAME'][i]) - 1:
				verbosePrint('.', verbose, end='')
			else:
				verbosePrint('', verbose)
		verbosePrint('QCLASS: %s' % p_response['QCLASS'][i][0], verbose)
		verbosePrint('QTYPE: %s' % p_response['QTYPE'][i][0], verbose)
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ANCOUNT_ANSWER':
				verbosePrint('############################################\nAnswer section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'NSCOUNT_ANSWER':
				verbosePrint('############################################\nAuthority section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ARCOUNT_ANSWER':
				verbosePrint('############################################\nAdditional section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	return success

def testOPCODEHandling(domainname, address, verbose):
	success = True
	packet = dnspacket.DNSPacket()
	packet.getStandardQueryOPCODEPacket(domainname)
	response = sendMessage(packet.getPacketBytes(), address)
	if response == None:
		verbosePrint('No response was received', verbose)
		return False
	p_response = packet.parseResponse(response)

	verbosePrint('############################################\nHeader:', verbose)
	#ID
	num = int(p_response['ID'], 2)
	verbosePrint('Header ID: %s ' % p_response['ID'], verbose)
		
	#QR
	num = int(p_response['QR'], 2)
	verbosePrint('QR: %s ' % p_response['QR'], verbose)
		
	#OPCODE
	num = int(p_response['OPCODE'], 2)
	verbosePrint('OPCODE: %s ' % p_response['OPCODE'], verbose, end='')
	if num == 0:
		verbosePrint(' (Standard Query)', verbose)
	elif num == 1:
		verbosePrint(' (Inverse Query)', verbose)
	elif num == 2:
		verbosePrint(' (Server Status Request)', verbose)
	else:
		verbosePrint(' (Reserved)', verbose)

	#AA
	verbosePrint('AA: %s ' % p_response['AA'], verbose)

	#TC
	verbosePrint('TC: %s' % p_response['TC'], verbose)

	#RD
	verbosePrint('RD: %s' % p_response['RD'], verbose)

	#RA
	verbosePrint('RA: %s' % p_response['RA'], verbose)

	#Z
	verbosePrint('Z: %s' % p_response['Z'], verbose)

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
	if num == 2 or num == 4:
		verbosePrint(' (OK)', verbose)
	else:
		verbosePrint(' (ERROR)', verbose)
		success = False
	
	#QDCOUNT
	verbosePrint('QDCOUNT: %s' % p_response['QDCOUNT'], verbose)
	
	#ANCOUNT
	verbosePrint('ANCOUNT: %s' % p_response['ANCOUNT'], verbose)

	#NSCOUNT
	verbosePrint('NSCOUNT: %s' % p_response['NSCOUNT'], verbose)

	#ARCOUNT
	verbosePrint('ARCOUNT: %s' % p_response['ARCOUNT'], verbose)

	for i in range(0, int(p_response['QDCOUNT'], 2)):
		verbosePrint('############################################\nQuestion section %i' % i, verbose)
		verbosePrint('QNAME: ', verbose, end='')
		for j, label in enumerate(p_response['QNAME'][i]):
			verbosePrint(label, verbose, end='')
			if j < len(p_response['QNAME'][i]) - 1:
				verbosePrint('.', verbose, end='')
			else:
				verbosePrint('', verbose)
		verbosePrint('QCLASS: %s' % p_response['QCLASS'][i][0], verbose)
		verbosePrint('QTYPE: %s' % p_response['QTYPE'][i][0], verbose)
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ANCOUNT_ANSWER':
				verbosePrint('############################################\nAnswer section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'NSCOUNT_ANSWER':
				verbosePrint('############################################\nAuthority section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ARCOUNT_ANSWER':
				verbosePrint('############################################\nAdditional section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	return success

def testZHandling(domainname, address, verbose):
	success = True
	packet = dnspacket.DNSPacket()
	packet.getStandardQueryZPacket(domainname)
	response = sendMessage(packet.getPacketBytes(), address)
	if response == None:
		verbosePrint('No response was received', verbose)
		return False
	p_response = packet.parseResponse(response)

	verbosePrint('############################################\nHeader:', verbose)
	#ID
	num = int(p_response['ID'], 2)
	verbosePrint('Header ID: %s ' % p_response['ID'], verbose)
		
	#QR
	num = int(p_response['QR'], 2)
	verbosePrint('QR: %s ' % p_response['QR'], verbose)
		
	#OPCODE
	num = int(p_response['OPCODE'], 2)
	verbosePrint('OPCODE: %s ' % p_response['OPCODE'], verbose, end='')
	if num == 0:
		verbosePrint(' (Standard Query)', verbose)
	elif num == 1:
		verbosePrint(' (Inverse Query)', verbose)
	elif num == 2:
		verbosePrint(' (Server Status Request)', verbose)
	else:
		verbosePrint(' (Reserved)', verbose)

	#AA
	verbosePrint('AA: %s ' % p_response['AA'], verbose)

	#TC
	verbosePrint('TC: %s' % p_response['TC'], verbose)

	#RD
	verbosePrint('RD: %s' % p_response['RD'], verbose)

	#RA
	verbosePrint('RA: %s' % p_response['RA'], verbose)

	#Z
	verbosePrint('Z: %s' % p_response['Z'], verbose)

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
	if not testValue(num, 1, verbose):
		success = False
	
	#QDCOUNT
	verbosePrint('QDCOUNT: %s' % p_response['QDCOUNT'], verbose)
	
	#ANCOUNT
	verbosePrint('ANCOUNT: %s' % p_response['ANCOUNT'], verbose)

	#NSCOUNT
	verbosePrint('NSCOUNT: %s' % p_response['NSCOUNT'], verbose)

	#ARCOUNT
	verbosePrint('ARCOUNT: %s' % p_response['ARCOUNT'], verbose)

	for i in range(0, int(p_response['QDCOUNT'], 2)):
		verbosePrint('############################################\nQuestion section %i' % i, verbose)
		verbosePrint('QNAME: ', verbose, end='')
		for j, label in enumerate(p_response['QNAME'][i]):
			verbosePrint(label, verbose, end='')
			if j < len(p_response['QNAME'][i]) - 1:
				verbosePrint('.', verbose, end='')
			else:
				verbosePrint('', verbose)
		verbosePrint('QCLASS: %s' % p_response['QCLASS'][i][0], verbose)
		verbosePrint('QTYPE: %s' % p_response['QTYPE'][i][0], verbose)
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ANCOUNT_ANSWER':
				verbosePrint('############################################\nAnswer section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'NSCOUNT_ANSWER':
				verbosePrint('############################################\nAuthority section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	try:
		i = 0
		for record in p_response['RR']:
			if record['RR_TYPE'] == 'ARCOUNT_ANSWER':
				verbosePrint('############################################\nAdditional section %i' % i, verbose)
				verbosePrint('NAME: ', verbose, end='')
				for j, label in enumerate(record['NAME']):
					verbosePrint(label, verbose, end='')
					if j < len(record['NAME']) - 1:
						verbosePrint('.', verbose, end='')
					else:
						verbosePrint('', verbose)
				verbosePrint('TYPE: %s' % record['TYPE'], verbose)
				verbosePrint('CLASS: %s' % record['CLASS'], verbose)
				verbosePrint('TTL: %i' % record['TTL'], verbose)
				verbosePrint('RDLENGTH: %i' % record['RDLENGTH'], verbose)
				verbosePrint('RDATA: %s' % record['RDATA'], verbose)
				i += 1
	except KeyError:
		pass
	
	return success
