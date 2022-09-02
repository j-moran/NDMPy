import func
import re

func.get_file_from_server('/usr/local/nagios/etc/objects/services.cfg', 'servicesTest.cfg')
func.get_file_from_server('/usr/local/nagios/etc/objects/servicegroups.cfg', 'servicegroups.cfg')

with open('servicesTest.cfg') as file:
	services_doc = file.read()

services_doc = services_doc.split('}')

with open('servicegroups.cfg') as file:
	servicegroup_doc = file.read()

servicegroup_doc = servicegroup_doc.split('}')

serviceDict = {}

for i,item in enumerate(servicegroup_doc):
	if (item != ''):
		srvgrp = ''
	else:
		continue

	split_item = item.split('\n')

	for j,chunk in enumerate(split_item):
		if (chunk == ''):
			continue
		if(re.search("^\s*servicegroup_name\s*.*$", chunk)):
			srvgrp = (split_item[split_item.index(chunk)].replace('servicegroup_name','')).strip()

	serviceDict[srvgrp] = {}

for i,item in enumerate(services_doc):
	if (item != ''):
		name = ''
		desc = ''
		srvgrp = ''
	else:
		continue

	split_item = item.split('\n')

	for j,chunk in enumerate(split_item):
		
		if (chunk == ''):
			continue
		if (re.search("^\s*name\s*.*$", chunk)):
			name = (split_item[split_item.index(chunk)].replace('name', '')).strip()
		if (re.search("^\s*service_description\s*.*$", chunk)):
			desc = (split_item[split_item.index(chunk)].replace('service_description','')).strip()
		if (re.search("^\s*servicegroups\s*.*$", chunk)):
			srvgrp = (split_item[split_item.index(chunk)].replace('servicegroups','')).strip()
			if (srvgrp not in serviceDict):
				serviceDict[srvgrp] = {}

	serviceDict[srvgrp][desc] = name

print(serviceDict)

#for key,value in serviceDict.items():
#	print(key + ' : ' + value)