# NDMPY - Nagios Device Manager
Nagios Core does not come with a way to manage and configure new devices without manually putting together a new configuration file each time you want to add a device.

I am seeking to build a relatively usable Python application that will allow you to build out configurations in a more streamlined way. Especially when creating many devices with similar needs.

## Prerequisites
- Python 3.10+
- Paramiko (At least version 2.11.0 - installed via pip)
- Nagios 4.6.0 (Tested, but should work on other versions as well)

## Getting Started
The best place to get started with this project is the installation guide located in the wiki. You can check it out [here](https://github.com/j-moran/NDMPy/wiki)!

### Nagios Setup
- Setup templates for services
- Setup object Structure

### NDM Setup
- Setup config file
- Setup service config


## Things to Do Still
- [x] Implement ability to remove modules from a config
- [ ] Create base configs from main menu
- [x] some sort of initialization process? In place. Simple checks for directories and checking connection to server
- [x] Actually write the getting started
- [ ] Clean up repo and make project more presentable
- [x] Try to pull existing service configurations from remote nagios server using servicegroups and service names
- [ ] Look into using configparser to handle config file
