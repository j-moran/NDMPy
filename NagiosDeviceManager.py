from csv import list_dialects
import os
import func, menus, config
from getpass import getpass

func.catch_c()
script_dir = os.path.dirname(__file__)

# Main loop - Main Menu
while (True):
	# Create main menu and generate options
	print(
		"------------------------------------------------------\n"
		"Main Menu\n"
		"------------------------------------------------------\n"
	)

	menus.main_menu()
	option = int(input('Please enter your choice: '))

	func.clear_screen()
	match option:
		case 1:
			# Receiving information about the device that is going to be added
			hostname = input('Please enter the hostname of the device you are trying to add: ')
			host_address = input('Please enter the IP address or FQDN (exampleHost.exampleDomain.com) of the device you are trying to add: ')
			func.clear_screen()

			# Displays the information entered previously
			func.current_config_host(hostname, host_address)

			# Generate the new configuration menu and wait for input from user
			while (True):
				items = menus.type_menu(config.device_types,True)
				option = int(input('Please enter your choice: '))
				device_to_create = func.check_selection(option,items,config.device_types)
				
				if((isinstance(device_to_create,dict)) and (device_to_create['name'])):
					# Generates the configuration choice menu (configuration from a base file or one where checks can be added a la carte)
					menus.config_menu()
					option = int(input('Please enter your choice: '))
					
					# Builds the configuration based on your previous choice. If a la carte option is picked a secondary menu will be generated
					#func.build_config(option,device_to_create,hostname,host_address)

					match option:
						# New Config from base configuration
						case 1:
							try:
								func.run_remote_command(f"cp {device_to_create['path']}/{device_to_create['basetype']}-base {device_to_create['path']}/{hostname}.cfg")
								func.run_remote_command(f"sed -i -e 's/\<base\>/{hostname}/g' {device_to_create['path']}/{hostname}.cfg")
								func.run_remote_command(f"sed -i -e 's/0.0.0.0/{host_address}/g' {device_to_create['path']}/{hostname}.cfg")

								print(
									'------------------------------------------------------\n'
									f"New configuration made with name {hostname}.cfg in {device_to_create['path']}. Please make any additional changes inside the file.\n"
									'------------------------------------------------------\n'
								)
							except:
								print("An error has occurred and a new configuration could not be saved.")

						# New custom config from available options
						case 2:
							#try:
								filename = f'{hostname}.cfg'
								service_menu = menus.build_service_menu(device_to_create['basetype'], device_to_create['OStype'])
								choice = int(input('Please enter your choice: '))

								# Initialize new configuration file locally
								default_config = [
									'define host {',
									f'host_name {hostname}',
									f'address {host_address}',
									f'use base_{device_to_create["OStype"]}_{device_to_create["platform"]}',
									'register 1',
									'}'
								]

								new_config = open(filename, 'w')
								with new_config as f:
									for line in default_config:
										f.write(line)
										f.write('\n')
								new_config.close()

								if(choice <= len(service_menu)):
									for i,opt in enumerate(service_menu):
										if(i + 1 == choice):
											choice = service_menu[opt]

									
								elif(choice == len(service_menu) + 1):
									func.clear_screen()
									break
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
							break

						case _:
							print('Please choose an option from the menu.')

					func.restart_nagios()
					break
				elif(device_to_create == 0):
					func.clear_screen()
					break
				else:
					print('Please choose an option from the menu.')

		case 3:
			print(script_dir)
			func.send_file_to_server(script_dir + '\config.py','/home/nagiosmanager/config.py')
			while (True):
				items = menus.type_menu(config.device_types) 							# Get the menu options from the generated menu
				option = int(input('Please enter your choice: ')) 	# Receive input about which device type to choose
				type_to_delete = func.check_selection(option,items,config.device_types)

				if((isinstance(type_to_delete,dict)) and (type_to_delete['name'])):
					# Generate the menu for the configuration deletion menu and receive input. del_menu returns the menu_options dictionary from the function for us later
					menu_items = menus.del_menu(type_to_delete['path'])
					location_path = type_to_delete['path']
					option = int(input('Please enter your choice: ')) # Here option is rewritten as a new selection. 
					
					# Checks to see if the selected option is apart of the configurations or is the menu option to exit that menu.
					# Runs a confirmation to make sure user wants to delete the configuration file they have selected.
					# Otherwise, it exits the menu
					if(option <= len(menu_items)):
						func.clear_screen()
						confirm = str(input(f"Are you sure you want to delete '{menu_items[option - 1]}'? (y/n)\n"))
							
						match confirm:
							case 'y' | 'Y':
								func.clear_screen()
								print(f"Config '{menu_items[option - 1]}' has been deleted")
								func.delete_config(location_path,menu_items[option - 1])
							case 'n' | 'N':
								break

					elif(option == len(menu_items) + 1):
						func.clear_screen()
						break
					else:
						print('Please choose an option from the menu.')
				elif(type_to_delete == 0):							
					func.clear_screen()
					break
				else:
					print('Please choose an option from the menu.')

		case 4:
			func.restart_nagios()
		case 5:
			func.clear_screen()
			break
		case _:
			print('Please choose an option from the menu.')