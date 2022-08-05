from os import path
batch_location = input("Please enter the full filepath for where you would like to have the NDMPy launcher.\n"
	"If you would like this to be placed on your desktop, please press the \'Enter\' key.\n"
) or 'Desktop'

NDMPy_location = path.dirname(__file__) + '\\NagiosDeviceManager.py'

if batch_location == 'Desktop' or batch_location == 'desktop':
	batch_location = path.expanduser("~") + '\Desktop\\NDMPy.bat'
else:
	batch_location += '\\NDMPy.bat'

with open(batch_location, 'a+') as file:
	file.write(f'python {NDMPy_location}')