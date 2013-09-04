#!/usr/bin/python

#Count the unique IP addresses of the BIND logfile and looks per domain

import sys
import operator
from operator import itemgetter

def main():

	#Reading the IP addresses from file
	domain_dict = {}
	for line in sys.stdin:
		if 'rate-limit' in line:

	#Extracting the IP address
			elements = line.split()
			ip_addr = elements[4].split('#')[0]
			domain = elements[13]		
	#Increase count
			if not domain_dict.has_key(domain):
				domain_dict[domain] = {}
			try:
				domain_dict[domain][ip_addr] += 1
			except:
				domain_dict[domain][ip_addr] = 1

	#writing output file
	print '{0:35} {1:35} {2:8}'.format('Domain', 'IP address', 'Count')
	print '-'*75			
	for domain in domain_dict.keys(): 
		for ip_addr in domain_dict[domain]:
		#print '\nDomain: %s' %  domain
		#for ip_addr in domain_dict[domain]:
			# dump addresses with counts
		#	print '%-40s (%s)' % (ip_addr, domain_dict[domain][ip_addr])
			print '{0:35} {1:35} {2:8}'.format(domain, ip_addr, domain_dict[domain][ip_addr])
	# done

if __name__ == "__main__":
	main()	
