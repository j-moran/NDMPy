from operator import contains
import func

func.get_file_from_server('/usr/local/nagios/etc/objects/services.cfg', 'servicesTest.cfg')

#with open('servicesTest.cfg', 'r') as file:
#	lines = file.readlines()

#lines = [line.strip() for line in lines]

with open('servicesTest.cfg') as file:
	doc = file.read()

doclist = doc.split('}')

serviceDict = {}

for i,item in enumerate(doclist):
	name_ind = 0
	desc_ind = 0

	split_item = item.split('\n')

	for j,chunk in enumerate(split_item):
		if (chunk == ''):
			continue
		if ('name ' in chunk):
			name_ind = j
		if ('service_description' in chunk):
			desc_ind = j
	name = (split_item[name_ind].replace('name', '')).strip()
	description = (split_item[desc_ind].replace('service_description','')).strip()
	serviceDict[description] = name

#print(doclist)

# Add Found Services to dictionary based on named services (Works but isn't maleable enough)
#serviceDict = {}

#for i,line in enumerate(lines):
#	if ('name' in line):
#		if('service_description' in lines[i+1]):
#			name = (line.replace('name', '')).strip()
#			description = (lines[i+1].replace('service_description','')).strip()
#			serviceDict[description] = name

#print(serviceDict)

#serviceDict = {}
#count = 0

#for i,line in enumerate(lines):
#	if (line == ''):
#		continue
#	if ('define service' in line):
#		count += 1
#		start_service = i
#	if (i >= start_service):
#		if('name' in line):
#			name = (line.replace('name', '')).strip()
#		if ('service_description' in line):
#			description = (line.replace('service_description','')).strip()
#			serviceDict[description] = name

#for key,value in serviceDict.items():	
#	for i,list in enumerate(value):
#		if (i > 0):
#			value[0] += value[i]
#	serviceDict[key] = value[0]

print(serviceDict)