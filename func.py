import config
import menus
import paramiko
import os
import signal
import re

#OS Commands
def run_remote_command(command):
	host = config.server_host

	try:
		conn = paramiko.SSHClient()
		conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		conn.connect(host,username=config.username,password=config.password)

		stdin, stdout, stderr = conn.exec_command(command)

		output = []

		if stderr.read() == b'':
			for line in stdout.readlines():
				output.append(line.strip())
			return output
		else:
			print(stderr.read())
	except:
		print("An error occurred while running command.")
	finally:
		if conn:
			conn.close()

def send_file_to_server(localfile,remotefile):
	host = config.server_host

	try:
		conn = paramiko.SSHClient()
		conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		conn.connect(host, username=config.username, password=config.password)

		ftp_client=conn.open_sftp()
		ftp_client.put(localfile,remotefile)
		ftp_client.close()

	#except:
	#	print("An error occurred while running command.")
	finally:
		if conn:
			conn.close()

def get_file_from_server(remotefile,localfile):
	host = config.server_host

	try:
		conn = paramiko.SSHClient()
		conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		conn.connect(host, username=config.username, password=config.password)

		ftp_client=conn.open_sftp()
		ftp_client.get(remotefile,localfile)
		ftp_client.close()

	#except:
	#	print("An error occurred while running command.")
	finally:
		if conn:
			conn.close()

def clear_screen():
	if os.name == "posix":
		os.system("clear")
	elif os.name == "nt":
		os.system("cls")

def restart_nagios():
	run_remote_command('sudo systemctl restart nagios.service')

def handler(signum, frame):
	clear_screen()
	exit(1)
		
def catch_c():
	signal.signal(signal.SIGINT, handler)

#Information
def current_config_host(hostname, host_address):
	print(
		"------------------------------------------------------\n"
		f"Current hostname is: {hostname}\n"
		f"Current host address is: {host_address}\n"
		"------------------------------------------------------\n"
	)

def check_selection(option,menu_items,dict):
	if(option <= len(dict)):				# Check to see if the selection is part of the device options
		option = menu_items[option]			# Change variable to reflect name of dictionary item
		option = dict[option]				# Grab the dictionary entry
		return option
	elif(option == len(menu_items)):		# This should be the menu option to quit/go back to the menu
		clear_screen()
		return 0


#Config Management
def generate_services(remote_service_config,remote_servicegroup_config):
	get_file_from_server(remote_service_config, 'services_local.cfg')
	get_file_from_server(remote_servicegroup_config, 'servicegroups_local.cfg')

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

def delete_config(location, config_to_delete):
	run_remote_command(f"rm {location}/{config_to_delete}")
	restart_nagios()

#def view_configs():
#	pass

def write_config(filename, lines):
	with open(filename, 'a+') as f:
		for line in lines:
			f.write(line)
			f.write('\n')


def send_config(filename, device_type):
	send = input(
			"Are you ready to send config to server? (y/n)\n"
			"NOTE: If you choose not to send to the server, the configuration will be discarded.\n"
		)

	match send:
		case 'y' | 'Y':
			if (os.path.exists(filename)):
				send_file_to_server(os.path.abspath(filename), device_type['path'] + f'/{filename}')
				os.remove(filename)
				clear_screen()

				print(
					'------------------------------------------------------\n'
					f"New configuration made with name {filename} in {device_type['path']}. Please make any additional changes inside the file.\n"
					'------------------------------------------------------\n'
				)
				return 0
		case 'n' | 'N':
			if (os.path.exists(filename)):
				os.remove(filename)
			clear_screen()
			return 0

def mod_module(filename, hostname, device_type, module_list, mod):
	service_menu = menus.build_service_menu(device_type['basetype'], device_type['OStype'], mod, module_list)
	choice = int(input('Please enter your choice: '))

	if ((choice <= len(service_menu)) and (choice != 0)):
		
		if (mod == 'add'):
			for i, opt in enumerate(service_menu):
				if (i + 1 == choice):
					choice = service_menu[opt]

			skeleton = [
				'define service {',
				f'host_name {hostname}',
				f'use {choice}',
				'register 1',
				'}'
			]

			write_config(filename, skeleton)
			clear_screen()

			print(
				'------------------------------------------------------\n'
				f'{key_value(choice, service_menu)} added to configuration.\n'
				'------------------------------------------------------\n'
			)
		elif (mod == 'delete'):
			target = 0

			for i, opt in enumerate(service_menu):
				if (i + 1 == choice):
					choice = service_menu[opt]
				
			with open(filename, 'r') as f:
				lines = f.readlines()

			for i,line in enumerate(lines):
					if choice in line:
						target = i - 2
						break
				
			for i in range(0,5):
				del lines[target]

			with open(filename, 'w') as f:
				for line in lines:
					f.write(line)

			clear_screen()

			print(
				'------------------------------------------------------\n'
				f'{key_value(choice, service_menu)} removed from configuration.\n'
				'------------------------------------------------------\n'
			)

		return choice

	elif ((choice == len(service_menu) + 1) or (choice == 0)):
		send_config(filename, device_type)
		return 0
	else:
		print('Please choose an option from the menu.')

#General Functions

def merge(*dicts):
	res = {}
	for dict in dicts:
		res = res | dict
	return res

def key_value(val, dict):
	for key, value in dict.items():
		if val == value:
			return key