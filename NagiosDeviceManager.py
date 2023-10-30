import os
import func
import menus
import config
import re

func.catch_c()
func.server_connect()
if(config.run_setup):
    func.setup()

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
                items = menus.type_menu(config.device_types, True)
                option = int(input('Please enter your choice: '))
                device_to_create = func.check_selection(option, items, config.device_types)

                if ((isinstance(device_to_create, dict)) and (device_to_create['name'])):
                    # Generates the configuration choice menu (configuration from a base file or one where checks can be added a la carte)
                    menus.config_menu()
                    option = int(input('Please enter your choice: '))

                    # Builds the configuration based on your previous choice. If a la carte option is picked a secondary menu will be generated

                    match option:
                        # New Config from base configuration
                        case 1:
                            new_config = f'{hostname}.cfg'
                            func.create_base_config(device_to_create)
                            func.get_file_from_server(f"{device_to_create['path']}/{device_to_create['basetype']}-base.cfg", new_config)

                            with open(new_config, 'r') as file:
                                lines = file.read()

                            lines = lines.split('}\n')

                            for i,line in enumerate(lines):
                                if (line == ''):
                                    lines.remove(lines[i])
                                else:
                                    lines[i] += '}\n'

                            for i,line in enumerate(lines):
                                if ('define host' in line):
                                    host_chunk = lines[i]

                                    host_chunk = host_chunk.split('\n')

                                    for j,chunk in enumerate(host_chunk):
                                        if(re.search("^\\s*host_name\\s*.*$", chunk)):
                                            host_chunk[j] = chunk.replace('base', hostname)
                                        if(re.search("^\\s*address\\s*.*$", chunk)):
                                            host_chunk[j] = chunk.replace('0.0.0.0', host_address)
                                        if(re.search("^\\s*register\\s*.*$", chunk)):
                                            host_chunk[j] = chunk.replace('0', '1')
                                        
                                        host_chunk[j] += '\n'

                                    host_chunk = "".join(host_chunk)
                                    lines[i] = host_chunk

                            lines = "".join(lines)

                            with open(new_config, 'w') as file:
                                file.write(lines)
                                    
                            func.send_file_to_server(new_config, f"{device_to_create['path']}/{new_config}")
                            os.remove(new_config)
                            func.restart_nagios()

                            print(
                                '------------------------------------------------------\n'
                                f"New configuration made with name {hostname}.cfg in {device_to_create['path']}.\n"
                                "Please make any additional changes inside the file or using the 'Modify Configurations' option in the main menu.\n"
                                '------------------------------------------------------\n'
                            )
                            
                        # New custom config from available options
                        case 2:
                            filename = f'{hostname}.cfg'
                            modules = []
                            # Initialize new configuration file locally
                            default_config = [
                                'define host {',
                                f'host_name {hostname}',
                                f'address {host_address}',
                                f'use base_{device_to_create["OStype"]}_{device_to_create["platform"]}',
                                'register 1',
                                '}'
                            ]

                            func.write_config(filename, default_config)
                            func.clear_screen()
                            while True:
                                new_module = func.mod_module(filename, hostname, device_to_create, modules, 'add')
                                
                                if(new_module == 0):
                                    break
                                else:
                                    modules.append(new_module)
                        case 3:
                            break

                        case _:
                            print('Please choose an option from the menu.')

                    func.restart_nagios()
                    break
                elif (device_to_create == 0):
                    func.clear_screen()
                    break
                else:
                    print('Please choose an option from the menu.')
        case 2:
            while True:
                items = menus.type_menu(config.device_types)
                option = int(input('Please enter your choice: '))
                type_to_modify = func.check_selection(option,items,config.device_types)

                func.clear_screen()

                print(
                    '------------------------------------------------------\n'
                    'Please choose the configuration you would like to modify:\n'
                    '------------------------------------------------------\n'
                )

                if ((isinstance(type_to_modify, dict)) and (type_to_modify['name'])):  # Choose config
                    menu_items = menus.config_list(type_to_modify['path'])
                    location_path = type_to_modify['path']
                    option = int(input('Please enter your choice: '))
                    filename = menu_items[option - 1]
                    hostname = filename.replace('.cfg', '')

                    func.clear_screen()

                    if (option <= len(menu_items)):  # if a config is chosen, are we adding or removing a module
                        func.get_file_from_server(type_to_modify['path'] + '/' + filename, filename)  # Get the config file from the server
                        config_modules = []
                        with open(filename) as file:  # read file into list per line
                            config_lines = file.readlines()
                            config_lines = [line.rstrip() for line in config_lines]

                        for line in config_lines:  # pull lines that contain modules and add them to new list
                            if 'use' in line:
                                line = line.strip()
                                config_modules.append(line.replace('use ', ''))
                        config_modules.pop(0)

                        menus.mod_menu()
                        mod_option = int(input('Please enter your choice: '))

                        func.clear_screen()

                        match mod_option:
                            case 1:  # if adding show a list of all modules and have user choose one to add
                                while True:
                                    new_module = func.mod_module(filename, hostname, type_to_modify, config_modules, 'add')
                                
                                    if(new_module == 0):
                                        func.restart_nagios()
                                        break
                                    else:
                                        config_modules.append(new_module)
                            case 2:  # Remove modules from config
                                while True:
                                    old_module = func.mod_module(filename, hostname, type_to_modify, config_modules, 'delete')

                                    if(old_module == 0):
                                        func.restart_nagios()
                                        break
                                    else:
                                        config_modules.remove(old_module)
                            case _:
                                pass
                    elif (option == len(menu_items) + 1):
                        func.clear_screen()
                        break
                    else:
                        print('Please choose an option from the menu.')
                elif (type_to_modify == 0):
                    func.clear_screen()
                    break
                else:
                    print('Please choose an option from the menu.')
            func.restart_nagios()
        case 3:
            while (True):
                items = menus.type_menu(config.device_types) 							# Get the menu options from the generated menu
                option = int(input('Please enter your choice: ')) 	# Receive input about which device type to choose
                type_to_delete = func.check_selection(option,items,config.device_types)

                if ((isinstance(type_to_delete, dict)) and (type_to_delete['name'])):
                    # Generate the menu for the configuration deletion menu and receive input. del_menu returns the menu_options dictionary from the function for us later
                    menu_items = menus.config_list(type_to_delete['path'])
                    location_path = type_to_delete['path']
                    option = int(input('Please enter your choice: ')) # Here option is rewritten as a new selection. 

                    # Checks to see if the selected option is apart of the configurations or is the menu option to exit that menu.
                    # Runs a confirmation to make sure user wants to delete the configuration file they have selected.
                    # Otherwise, it exits the menu
                    if (option <= len(menu_items)):
                        func.clear_screen()
                        confirm = str(input(f"Are you sure you want to delete '{menu_items[option - 1]}'? (y/n)\n"))

                        match confirm:
                            case 'y' | 'Y':
                                func.clear_screen()
                                print(f"Config '{menu_items[option - 1]}' has been deleted")
                                func.delete_config(location_path, menu_items[option - 1])
                            case 'n' | 'N':
                                break

                    elif (option == len(menu_items) + 1):
                        func.clear_screen()
                        break
                    else:
                        print('Please choose an option from the menu.')
                elif (type_to_delete == 0):
                    func.clear_screen()
                    break
                else:
                    print('Please choose an option from the menu.')
        case 4:
            func.restart_nagios()
        case 6:
            func.clear_screen()
            break
        case _:
            print('Please choose an option from the menu.')
