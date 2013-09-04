#initcode

import os
import re

def get_modnames(directory):
	modnames = []
	for root, dirs, files in os.walk(directory):
		for filename in files:
			if re.match(r'mod_.*.py$', filename):
				modnames.append(filename[0:-3])
	return modnames

if __name__ == "__main__":
	modnames = get_modnames("./modtest/modules")
	my_modules = []
	for modname in modnames:
		my_modules.append(__import__('modules.%s' % modname, fromlist=[modname]))
		print(my_modules[-1].getModuleName())
		my_modules[-1].initMod()
		
