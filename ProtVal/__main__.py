#=====================================================================
#filename       : __main__.py
#description    : Main function of ProtVal
#python_version : 3.x
#internal notes : see bottom of script
#=====================================================================

import os
import re

#Returns true if the number can be cast to an integer. False otherwise
def is_integer(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

#Returns a string list of all files in the ./modules directory starting with mod_ and ending with .py
def get_modnames(directory):
	modnames = []
	for item in os.listdir(directory):
		if re.match(r'^mod_.*\.py$', item):
			modnames.append(item[0:-3])
	return modnames

#Obtains a list of all ProtVal modules and attempts to load them
def main():
	modnames = get_modnames(os.path.dirname(os.path.realpath(__file__)) + "/modules")
	loaded_modules = []

	for modname in modnames:
		#Attempt to load the module and check if it contains the required functions
		try:
			module = __import__('modules.%s' % modname, fromlist=[modname])
			if hasattr(module, "getModuleName") and hasattr(module, "getModuleDescription") and hasattr(module, "initMod"):
				loaded_modules.append(__import__('modules.%s' % modname, fromlist=[modname]))
		except ImportError:
			print("Error importing %s" % modname)
	
	if len(loaded_modules) <= 0:
		print("No modules found. Exiting...")
		os.sys.exit()
	else:
		#Display all module names and descriptions
		print("Modules found:")

		i = 1
		for module in loaded_modules:
			print(str(i) + ". " + module.getModuleName() + " - " + module.getModuleDescription())
			i += 1

		#Try to get the user to pick a number corresponding to one of the modules printed above.
		#Then convert the number to the corresponding list index.
		choice = 0
		while True:
			answer = input("Please enter a module to use [1 - " + str(len(loaded_modules)) + "]: ")
			if is_integer(answer):
				choice = int(answer)
				if choice > 0 and choice <= len(loaded_modules):
					choice -= 1
					break

		loaded_modules[choice].initMod()

if __name__ == "__main__":
	main()		

"""
Internal notes:
At this point, the following DNS section formats of DNS are supported:
Header, Question, Answer, Authority, Additional

Parser supports the following fields in the header section format:
Header:
ID (16bits; Identifier, copied matching the corresponding reply)
QR (1 bit; Must be 0 (query) or 1 (response))
OPCODE (4 bits; Specified kind of query, 0 standard QUERY, 1 inverse IQUERY, 2 server status (STATUS), reserved 3-15)
AA (1 bit) 	(Authorative Answer, specifief if it is an answer)
TC (1 bit)	(Truncation, message is truncated)
RD (1 bit)	(Recursion desired, this bit may be set in a query and is copied in the response)
RA (1 bit)	(Recursion avaiable, this be is set or cleared in a response, if recursive query is supported on the name server)
Z  (3 bits)	(Reserved for future use, must be zero in all queries)	
RCODE (4 bits)	(0 no error, 1 format error - the name server was unable to interpret the query, 2 server failure - the name server was unable to process this query due to a problem with the name server, 3 - name error, meaninful only for response from an authorative name server this code signifies in the query does not exist, 4 - not implemented the server does not support the requested kinds of query, 5 refused - the name server refuses to perform the specified operation for policy reasons)
QDCOUNT (16 bits)	(An unsigned 16 bit integer specifying the number of entries in the question section)
ANCOUNT (16 bits)	(An unsigned 16 bit integer specifying the number of resource records in the answer section)
NSCOUNT (16 bits)	(An unsigned 16 bit integer specifying the number of name server resource records in the authority records section)
ARCOUNT (16 bits)	(An unsigned 16 bit integer specifying the number of resource records in the addition records section)

Question Section Format:
QNAME (16 bit; domain name represented as a sequence of labels, where each label consists of a length octet followed by that number ofectest)
QTYPE (16 bit; a two octet code which specifies the type of the query; the value for this field include all codes valid for a TYPE field, together with some more general codes which can match more than one type of RR)
QCLASS (16 bit; a two octet code that specifies the class of the query (e.g. QCLASS field is IN for the Internet)

Resource Record Format:
NAME (variable length; a domain name to which this resource record pertains)
TYPE (16 bit; two octets containing one of the RR type codes; this field specifies the meaning of the data in the RDATA field)
CLASS (16 bit: two octets which specify the class of the data in the RDATA field)
TTL (32 bit: unsigned integer that specifies the time interval (in sec) that the resource record may be cached before it should be discarded; zero values are interpreted to mean that the RR can only be used for the transaction in progress, and should not be cached)
RDLENGTH (16 bit: unsigned integer that specifies the length in octets of the RDATA field)
RDATA (variable length): string of octets that describes the resource (format of this information varies according to the TYPE and CLASS of the resource record, e.g. if the TYPE is A, and the class is IN, the RDATA field is a 4 octet ARPA Internet address)

Parser improvements:
Use structs for parsing the data and length to determine the length of a possible domainname or IP-address (4 (octect) for IPv4).
Example:
data_struct = struct.Struct("<2H") #example
data_unpacked = struct.unpack(format, data)
Possible struct formats:
b (8-bit signed integer)
B (8-bit unsigned integer)
h (16-bit signed integer)
H (16-bit unsigned integer)
i (32-bit signed integer)
I (32-bit unsigned integer)
q (64-bit signed integer)
Q (64-bit unsigned integer
f (32-bit float)
d (64-bit float)
? (Boolean)
s (bytes or bytearray object)

Not implemented:
There is no TCP validation at the moment.

Not implemented fields:

    0                   1                   2                   3   
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version|  IHL  |Type of Service|          Total Length         |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Identification        |Flags|      Fragment Offset    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Time to Live |    Protocol   |         Header Checksum       |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                       Source Address                          |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Destination Address                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Future work, parse the TCP/IP header as follows:
sock_client = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
packet = sock_client.recvfrom(65565)
packet = packet[0] #This must be done because we receive a tuple
ip_header = packet[0:20]
iph = unpack('!BBHHHBBH4s4s' , ip_header)
version = version_ihl >> 4
ihl = version_ihl & 0xF #use bitmask in order to get the length of the IP packet
iph_length = ihl * 4 #According to the RFC we must multiply it by 4 to get the real length

tcp_header = packet[iph_length:iph_length+20] #get the tcp header using the length that we have justed calculated

tcph = unpack('!HHLLBBHHH' , tcp_header)
source_port = tcph[0]
dest_port = tcph[1]

acknowledgement = tcph[3]
off_reserved = tcph[4]
tcph_length = off_reserved >> 4

h_size = iph_length + tcph_length * 4
data_size = len(packet) - h_size
     
#get data from the packet
data = packet[h_size:]

If data is a string we can, for example, the following:
data.decode()
Of if we know what data contains we can use a struct
test = struct.Struct(">2s")
#data = b'tt'
data_unpack = test.struct(data)[0].decode() #Unpack returns tuple, we only want the first item and decode the string.
"""