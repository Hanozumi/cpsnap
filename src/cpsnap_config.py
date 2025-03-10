'''
	cpsnap_config.py
	configuration manager and parser

	Copyright © 2025 Hanozumi
'''

import csv

class Config:
	'''Config class for managing .conf files.

	Attributes:
		source_paths (list): List of source paths.
		backup_path (str): Single backup path (remote, if ssh_path set).
		ssh_path (str): Path to remote ssh server.
		ssh_certs_path (str): Path to ssh certs for remote server.
		retains (dict): Dictionary of retain configurations.
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
			- backup_path (str): Single backup path (remote, if ssh_path set).
			- ssh_path (str) | None: Path to remote ssh server.
			- ssh_certs_path (str) | None: Path to ssh certs for remote server.
			- retains (dict): Dictionary of retain configurations.

		Raises:
			ValueError: An invalid configuration options has been set or a configuration option is missing.
		'''

		self.source_paths = []
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
					case 'backup': self.backup_path = filtered[1]
					case 'ssh': self.ssh_path = filtered[1]
					case 'ssh_certs': self.ssh_certs_path = filtered[1]
					case 'retain': self.retains[filtered[1]] = filtered[2:]
					case _: print(f'Unknown configuration option "{filtered[0]}"')

		if len(self.source_paths) <= 0: raise ValueError("At least one source path needs to be set.")
		if len(self.backup_path)  <= 0: raise ValueError("A backup path needs to be set.")
		if len(self.retains)	  <= 0: raise ValueError("At least one retain option needs to be set.")