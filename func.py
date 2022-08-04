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

def delete_config(location, config_to_delete):
	run_remote_command(f"rm {location}/{config_to_delete}")
	restart_nagios()

def view_configs():
	pass

def write_config(filename, lines):
	with open(filename, 'a+') as f:
		for line in lines:
			f.write(line)
			f.write('\n')

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