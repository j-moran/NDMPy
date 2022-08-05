from os import path
batch_location = input("Please enter the full filepath for where you would like to have the NDMPy launcher.\n"
	"If you would like this to be placed on your desktop, please enter \"Desktop\"\n"
)

NDMPy_location = r'%s' % path.dirname(__file__)
NDMPy_location.replace("\\", "/")
NDMPy_location += '\\NagiosDeviceManager.py'

match batch_location:
	case 'Desktop' | 'desktop':
		batch_location = path.expanduser("~") + '\Desktop'
		batch_location.replace("\\", "/")

		with open(batch_location + '\\NDMPy.bat', 'a+') as file:
			file.write(f'python {NDMPy_location}')