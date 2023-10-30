import func
import config
import re
import os
import paramiko

def server_connect(command = 'pass'):
	errors = []
	try:
		conn = paramiko.SSHClient()
		conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		conn.connect(config.server_host,username=config.username,password=config.password)

		if (command != 'pass'):
			stdin, stdout, stderr = conn.exec_command(command)
			
			out = []
			err = stderr.readlines()

			for line in stdout.readlines():
				out.append(line.strip())

			return out, err

	except paramiko.SSHException as SSHerror:
		SSHerror = "ERROR: A connection error occurred while connecting to Nagios server: " + str(SSHerror)
		errors.append(SSHerror)
	except TimeoutError:
		errors.append("ERROR: Connection timed out while connecting to server. Please check config to make sure the server address is correct.")
	finally:
		if (conn):
			conn.close()
		if (len(errors) > 0):
			for error in errors:
				print(error)
			exit()

server_connect()