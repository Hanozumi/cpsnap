'''
	cpsnap_config.py
	configuration manager and parser

	Copyright © 2025 Hanozumi
'''

import csv

class Retain:
	'''Helper class to maintain retain options readability.

	Attributes:
		type (str): Type of retain.
		num (int): Number of retained backups.
		mode (str): Backup mode.
		name_func (str): Selected backup naming function.
	'''
	def __init__(self, type:str, num: int, mode: str, name_func: str):
		'''Prepare a Retain-object, with given attributes.

		Args:
			type (str): Type of retain.
			num (int): Number of retained backups.
			mode (str): Backup mode.
			name_func (str): Selected backup naming function.
		'''
		self.type = type
		self.num = num
		self.mode = mode
		self.name_func = name_func

class Config:
	'''Config class for managing .conf files.

	Attributes:
		source_paths (list): List of source paths.
		excludes (list): List of excluded folders and files
		backup_path (str): Single backup path (remote, if ssh_path set).
		ssh_path (str): Path to remote ssh server.
		ssh_certs_path (str): Path to ssh certs for remote server.
		retains (dict[str, Retain]): Dictionary of retain objects.
	'''

	def __init__(self, config_path: str, c_char: str, delimiter: str):
		'''Prepares a given config file and returns usable information as Config object.

		Args:
			config_path (str): Path to config file.
			c_char (str): Comment char of config file.
			delimiter (str): Delimiter/Split char of config file.

		Returns:
			out (Config): Config object including
			- source_paths (list): List of source paths.
			- excludes (list): List of excluded folders and files
			- backup_path (str): Single backup path (remote, if ssh_path set).
			- ssh_path (str) | None: Path to remote ssh server.
			- ssh_certs_path (str) | None: Path to ssh certs for remote server.
			- retains (dict[str, Retain]): Dictionary of retain objects.

		Raises:
			ValueError: An invalid configuration options has been set or a configuration option is missing.
		'''

		self.source_paths = []
		self.excludes = [] 				# !!!
		self.backup_path = ''
		self.ssh_path = ''
		self.ssh_certs_path = ''
		self.retains = {  }

		with open(config_path) as conf:
			conf_raw = []
			for row in conf:
				raw = row.split(c_char)[0].strip()
				if raw != '': conf_raw.append(raw)

			for line in csv.reader(conf_raw, delimiter=delimiter):
				filtered = list(filter(lambda x: x.strip(), line))
				match filtered[0]:
					case 'source': self.source_paths.append(filtered[1])
					case 'excludes': self.excludes = [e.strip() for e in filtered[1].split(',')]
					case 'backup': self.backup_path = filtered[1]
					case 'ssh': self.ssh_path = filtered[1]
					case 'ssh_certs': self.ssh_certs_path = filtered[1]
					case 'retain': 
						if len(filtered) != 5: 
							raise ValueError(f'Invalid number of retain options for "{filtered[1]}". Needs retain <type> <num> <mode> <name_func>.')
						self.retains[filtered[1]] = Retain(filtered[1], int(filtered[2]), filtered[3], filtered[4])
					case _: print(f'Unknown configuration option "{filtered[0]}"')

		if len(self.source_paths) <= 0: raise ValueError('At least one source path needs to be set.')
		if len(self.backup_path)  <= 0: raise ValueError('A backup path needs to be set.')
		if len(self.retains)	  <= 0: raise ValueError('At least one retain option needs to be set.')