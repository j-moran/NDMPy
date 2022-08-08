import func
import services

# Menus


def generate_menu(menu_options):
    for key in menu_options.keys():
        print(key, ' - ', menu_options[key])


def main_menu():
    menu_options = {
        1: 'Create a new device configuration',
        2: 'Modify an existing configuration',
        3: 'Delete an existing configuration',
        4: 'Restart Nagios Service',
        5: 'Quit'
    }

    generate_menu(menu_options)


def type_menu(dict, mod=False):
    menu_options = {}

    for i, item in enumerate(dict):
        menu_options[i + 1] = item

    if (mod):
        menu_options[list(menu_options)[-1] + 1] = 'Modify device information'

    menu_options[list(menu_options)[-1] + 1] = 'Quit'

    print(
        '------------------------------------------------------\n'
        'Please choose the type of device:\n'
        '------------------------------------------------------\n'
    )

    generate_menu(menu_options)
    return menu_options


def build_service_menu(service, OS, *configfile):
    service = service + '_services'
    OS = OS + '_services'

    combined_list = func.merge(
        services.service_types[service],
        services.service_types[OS],
        services.service_types['general_services']
    )

    if (configfile):
        for file in configfile:
            for item in file:
                del combined_list[func.key_value(item, combined_list)]

    type_menu(combined_list)

    return combined_list


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


def network_menu():
    menu_options = {
        1: 'Router (Not Available Yet)',
        2: 'Switch',
        3: 'AP (Access Point) (Not Available Yet)',
        4: 'Firewall (Not Available Yet)',
        5: 'Quit'
    }

    generate_menu(menu_options)


def config_list(loc):
    configs_from_loc = func.run_remote_command(fr"ls {loc} | egrep '\.cfg$'")
    menu_options = {}

    for i, config in enumerate(configs_from_loc):
        menu_options[i + 1] = config

    menu_options[list(menu_options)[-1] + 1] = 'Quit'
    generate_menu(menu_options)
    return configs_from_loc


def mod_menu():
    menu_options = {
        1: 'Add Module to Config',
        2: 'Remove Module from Config',
        3: 'Quit'
    }

    generate_menu(menu_options)
