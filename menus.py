import func
import config

# Menus

# Main function for generating menus. Takes menu_options as input from functions that call it.
def generate_menu(menu_options):
    for key in menu_options.keys():
        print(key, ' - ', menu_options[key])


# Main application menu
def main_menu():
    menu_options = {
        1: 'Create a new device configuration',
        2: 'Modify an existing configuration',
        3: 'Delete an existing configuration',
        4: 'Restart Nagios Service',
        5: 'Additional Options',
        6: 'Quit'
    }

    generate_menu(menu_options)


# Generates the menu for most sub processes that deal with listing items from Nagios server (Configs, services, etc.)
def type_menu(dict, mod=False):
    menu_options = {}

    for i, item in enumerate(dict):
        menu_options[i + 1] = item

    if (mod):
        menu_options[list(menu_options)[-1] + 1] = 'Modify device information'

    if (menu_options):
        menu_options[list(menu_options)[-1] + 1] = 'Quit'
    else:
        menu_options[0] = 'Quit'

    generate_menu(menu_options)
    return menu_options


# Takes several inputs in order to create the menu list for services available either to add or delete from a config
def build_service_menu(service, OS, mod = '', *configfile):
    service_types = func.generate_services(config.service_config, config.servicegroup_config)
    service = service + '_services'
    OS = OS + '_services'

    combined_list = func.merge(
        service_types[service],
        service_types[OS],
        service_types['general_services']
    )

    if (configfile):
        match mod:
            case 'add':
                for file in configfile:
                    for item in file:
                        del combined_list[func.key_value(item, combined_list)]
                
                type_menu(combined_list)
                return combined_list

            case 'delete':
                del_list = {}
                for file in configfile:
                    for module in file:
                        if module in combined_list.values():
                            del_list[func.key_value(module, combined_list)] = module

                type_menu(del_list)
                return del_list


# Static menu for whether to create a new config from a base or from scratch
def config_menu():
    menu_options = {
        1: 'Base Configuration',
        2: 'Custom Configuration',
        3: 'Quit'
    }

    print(
        '------------------------------------------------------\n'
        'Would you like to use the base configuration or build your own?\n'
        '------------------------------------------------------\n'
    )

    generate_menu(menu_options)

# Menu for the network device type to be added (STILL IN PROGRESS)
def network_menu():
    menu_options = {
        1: 'Router (Not Available Yet)',
        2: 'Switch',
        3: 'AP (Access Point) (Not Available Yet)',
        4: 'Firewall (Not Available Yet)',
        5: 'Quit'
    }

    generate_menu(menu_options)


# Creates the menu options that list all configs of a certain device type
def config_list(loc):
    configs_from_loc = func.server_connect(fr"ls {loc} | egrep '\.cfg$'")
    menu_options = {}

    for i, config in enumerate(configs_from_loc):
        menu_options[i + 1] = config

    menu_options[list(menu_options)[-1] + 1] = 'Quit'
    generate_menu(menu_options)
    return configs_from_loc

# Static menu for either adding or removing a service mdule to/from a config
def mod_menu():
    menu_options = {
        1: 'Add Module to Config',
        2: 'Remove Module from Config',
        3: 'Quit'
    }

    generate_menu(menu_options)
