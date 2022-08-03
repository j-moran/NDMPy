import config, menus
import paramiko
import os, signal

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
def build_config(option,type,hostname,host_address):
	match option:
		# New Config from base configuration
		case 1:
			try:
				run_remote_command(f"cp {type['path']}/{type['basetype']}-base {type['path']}/{hostname}.cfg")
				run_remote_command(f"sed -i -e 's/\<base\>/{hostname}/g' {type['path']}/{hostname}.cfg")
				run_remote_command(f"sed -i -e 's/0.0.0.0/{host_address}/g' {type['path']}/{hostname}.cfg")

				print(
					'------------------------------------------------------\n'
					f"New configuration made with name {hostname}.cfg in {type['path']}. Please make any additional changes inside the file.\n"
					'------------------------------------------------------\n'
				)
			except:
				print("An error has occurred and a new configuration could not be saved.")

		# New custom config from available options
		case 2:
			#try:
				filename = f'{hostname}.cfg'
				service_menu = menus.build_service_menu(type['basetype'], type['OStype'])
				choice = int(input('Please enter your choice: '))

				#print(service_menu)

				if(choice <= len(service_menu)):
					for i,opt in enumerate(service_menu):
						if(i + 1 == choice):
							choice = service_menu[opt]

					
				elif(choice == len(service_menu) + 1):
					clear_screen()
					return 0
				else:
					print('Please choose an option from the menu.')

				#print(
				#	'------------------------------------------------------\n'
				#	f"New configuration made with name {hostname}.cfg in {type['path']}. Please make any additional changes inside the file.\n"
				#	'------------------------------------------------------\n'
				#)
			#except:
				#print("An error has occurred and a new configuration could not be saved.")				
		case 3:
			return 0

		case _:
			print('Please choose an option from the menu.')

	restart_nagios()

def delete_config(location, config_to_delete):
	run_remote_command(f"rm {location}/{config_to_delete}")
	restart_nagios()

def view_configs():
	pass

#General Functions

def merge(*dicts):
	res = {}
	for dict in dicts:
		res = res | dict
	return res