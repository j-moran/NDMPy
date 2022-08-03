#host config - ALL DATA STORED IN PLAINTEXT!!!! PLEASE CREATE USER WITH LIMITED ACCESS IN ORDER TO USE THIS APP!!!
server_host 	= '10.2.15.100'
username 		= 'nagiosmanager'
password		= 'N@giosM4n'

#Nagios Object Dictionaries
device_types = {
	'Windows Server' : {
		'name' 			:	'Windows Server',
		'path'		 	: 	'/usr/local/nagios/etc/objects/windows/servers',
		'basetype'	 	: 	'windows_server',
		'OStype'  	 	: 	'windows',
		'platform'	 	:	'server'
		}
}

winDeskLoc		= '/usr/local/nagios/etc/objects/windows/desktops'
winLapLoc		= '/usr/local/nagios/etc/objects/windows/laptops'
ciscoSWLoc		= '/usr/local/nagios/etc/objects/cisco/switches'
ciscoAPLoc		= '/usr/local/nagios/etc/objects/cisco/APs'
storageLoc		= '/usr/local/nagios/etc/objects/storage'