'''
	cpsnap.py
	simple backup and snapshot CLI utility for local and remote/ssh usage

	Copyright © 2025 Hanozumi
'''

import os
import argparse
import paramiko
import getpass
from cpsnap_config import Config, Retain
import cpsnap_helper

valid_retain_modes = ('h', 'f')
valid_retain_name_funcs = ('date', 'datetime', 'weekday')

os.chdir(os.path.dirname(__file__))

# argparse
parser = argparse.ArgumentParser(description='Simple backup and snapshot CLI utility for local and remote/ssh usage.')
parser.add_argument('retain', metavar='retain', type=str, help='name of the retain type to be executed')
parser.add_argument('-q', action=argparse.BooleanOptionalAction, help='enable QT tray icon (only needed if run with active Desktop Environment)')
parser.add_argument('-t', action=argparse.BooleanOptionalAction, help='Only print outputs; do not run destructive commands.')
parser.add_argument('-c', '--config', metavar='config', type=str, help='path to custom config file')
args = parser.parse_args()

if args.t: print('\n=== Running in test-mode ===\n')

# config load
config_path = args.config if args.config != None else 'conf/default.conf'
config = Config(config_path, '#', '\t')

print(f'Using config: {config_path}\n')

# check selected retain availability
if args.retain not in config.retains: raise ValueError(f'Retain type "{args.retain}" is not configured.')

# check retain completeness and validity
print('Valid retains: [selected]')

selected_retain = None
for retain in config.retains:
	retain_o: Retain
	retain_o = config.retains[retain]
	if retain_o.mode not in valid_retain_modes:
		raise ValueError(f'Invalid retain mode: {retain_o.mode}.')
	elif retain_o.name_func not in valid_retain_name_funcs:
		raise ValueError(f'Invalid retain naming-function: {retain_o.name_func}.')
	
	if retain == args.retain:
		print(f'- [{retain}] => num: {retain_o.num}, mode: {retain_o.mode}, name_func: {retain_o.name_func}')
		selected_retain = retain_o
	else:
		print(f'- {retain}')

print()
# check source validity
print('Source directories:')

for path in config.source_paths:
	if not os.path.isdir(path): raise FileNotFoundError(f'The directory "{path}" does not exist.')
	print(f'- {path}')

# if applicable, connect ssh (with certs)
if config.ssh_path != '':
	ssh_username, ssh_hostname = config.ssh_path.split('@')
	ssh = paramiko.SSHClient()
	if config.ssh_certs_path != '':
		try:
			ssh_key = paramiko.Ed25519Key.from_private_key_file(config.ssh_certs_path)
		except:
			raise paramiko.SSHException('ssh_certs needs to point to a valid ed25519 encoded private key.')
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=ssh_hostname, username=ssh_username, pkey=ssh_key)
	else:
		ssh_pass = getpass.getpass(f'\nEnter password for {ssh_username}@{ssh_hostname}: ')
		ssh.connect(hostname=ssh_hostname, username=ssh_username, password=ssh_pass)

	print()
	print(f'Valid SSH connection @ {config.ssh_path}.')

# create backup parent dir if not exist
cpsnap_helper.ask_create_r_u_dir(config.backup_path,
								 f'\nThe backup path {config.backup_path} does not exist.\nCreate it?',
								 args.t)

# create backup type dir if not exist
backup_type_path = os.path.join(config.backup_path, args.retain)
cpsnap_helper.create_r_u_dir(backup_type_path, args.t)

# get current backup count
current_type_backup_count = -1
if not args.t:
	current_type_backup_count = len(os.listdir(backup_type_path))

print(f'Backup directory: {backup_type_path}', '[{n:0{width}d}/{m}]'.format(n=current_type_backup_count,
																			width=len(str(selected_retain.num)),
																			m=selected_retain.num))

## EXECUTE BACKUP; TODO ##