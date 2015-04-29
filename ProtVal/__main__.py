#=====================================================================
#filename       : __main__.py
#description    : Main function of ProtVal
#python_version : 3.x
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
	try:
		main()
	except KeyboardInterrupt:
		print('\nGoodbye!')
