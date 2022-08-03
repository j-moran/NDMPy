service_types = {
	'general_services': {
		'Device IP Address': 'get_ip',
		'Ping Check': 'ping_check'
	},
	'windows_services': {
		'NCPA Agent Version': 'agent_version',
		'SEP Service Check': 'wdp_sep_check',
		'CPU Usage Check': 'wdp_cpu_usage',
		'RAM Usage Check': 'wdp_ram_usage',
		'Disk Usage Check': 'wdp_disk_usage'
	},
	'windows_server_services': {
		'Windows Server Uptime Check': 'wdp_server_uptime'
	},
	'windows_desktop_services': {
		'Windows Desktop Uptime Check': 'wdp_desktop_uptime'
	},
	'storage_services': {
		'Synology Status Check':'synology_check'
	}
}