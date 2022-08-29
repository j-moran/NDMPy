from operator import contains
import func

func.get_file_from_server('/usr/local/nagios/etc/objects/services.cfg', 'servicesTest.cfg')

with open('servicesTest.cfg', 'r') as file:
	lines = file.readlines()

lines = [line.strip() for line in lines]

# Add Found Services to dictionary based on named services (Works but isn't maleable enough)
serviceDict = {}

for i,line in enumerate(lines):
	if ('name' in line):
		if('service_description' in lines[i+1]):
			name = (line.replace('name', '')).strip()
			description = (lines[i+1].replace('service_description','')).strip()
			serviceDict[description] = name

print(serviceDict)

#serviceDict = {}
#count = 0

#for i,line in enumerate(lines):
#	if (line == ''):
#		continue
#	if ('define service' in line):
#		count += 1
#		start_service = i
#		serviceDict[count] = []
#	if (i >= start_service):
#		if (('name' in line) or ('service_description' in line) or ('servicegroup' in line)):
#			serviceDict[count].append([line])

#for key,value in serviceDict.items():	
#	for i,list in enumerate(value):
#		if (i > 0):
#			value[0] += value[i]
#	serviceDict[key] = value[0]

#print(serviceDict)