# NDMPY - Nagios Device Manager
Nagios Core does not come with a way to manage and configure new devices without manually putting together a new configuration file each time you want to add a device.

I am seeking to build a relatively usable Python application that will allow you to build out configurations in a more streamlined way. Especially when creating many devices with similar needs.

## Prerequisites
- Python 3.10+
- Paramiko (At least version 2.11.0 - installed via pip)
- Nagios 4.6.0 (Tested, but should work on other versions as well)

## Getting Started

### Nagios Setup
- Setup templates for services
- Setup object Structure

### NDM Setup
- Setup config file
- Setup service config


## Things to Do Still
- [x] Implement ability to remove modules from a config
- [ ] Create base configs from main menu
- [ ] some sort of initialization process? (This is a maybe. Most things should be taken care of in the getting started...)
- [ ] Actually write the getting started
    - [ ] Setting up Services
    - [ ] Setting up device templates
- [ ] Clean up repo and make project more presentable