'''
	cpsnap_config.py
	configuration manager and parser

	Copyright © 2025 Hanozumi
'''

import csv

source_paths = []
backup_path = ''
ssh_path = ''
retains = []

def prepare_config(config_path: str, c_char: str, delimiter: str) -> tuple[list, str, str, list]:
	'''Prepares a given config file and returns usable information on configuration.

	Args:
		config_path (str): Path to config file
		c_char (str): Comment char of config file
		delimiter (str): Delimiter/Split char of config file

	Returns:
		out (tuple): tuple containing
		- source_paths (list): List of source paths
		- backup_path (str): Single backup path (remote, if ssh_path set)
		- ssh_path (str) | None: Path to remote ssh server
		- retains (list): List of retain configurations
	'''

	with open(config_path) as conf:
		conf_raw = []
		for row in conf:
			raw = row.split(c_char)[0].strip()
			if raw != '': conf_raw.append(raw)

		for line in csv.reader(conf_raw, delimiter=delimiter):
			filtered = list(filter(lambda x: x.strip(), line))
			match filtered[0]:
				case 'source': 	source_paths.append(filtered[1])
				case 'backup': 	backup_path = filtered[1]
				case 'ssh': 	ssh_path = filtered[1]
				# case 'retain'
				case _: 		print(f'Unknown configuration option "{filtered[0]}"')

	return source_paths, backup_path, ssh_path, retains