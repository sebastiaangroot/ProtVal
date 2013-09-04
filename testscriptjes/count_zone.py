#!/usr/bin/python

import sys

def main():
	infilename = sys.stdin
	non_ripe_dict = {}
	for line in infilename:
		elements = line.split()
		if 'rate-limit' in line:
			zone = elements[13]
			if not ('ripe.net' and 'secret-wg.org') in line:
				if zone in non_ripe_dict:
					non_ripe_dict[zone] += 1
				else:
					non_ripe_dict[zone] = 1
	for zone, count in non_ripe_dict.iteritems():
		print 'Count of Zones: %s (%s)' % (count, zone)

if __name__ == "__main__":
	main()
