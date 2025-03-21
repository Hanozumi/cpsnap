'''
	cpsnap_helper.py
	cpsnap helper functions

	Copyright © 2025 Hanozumi
'''

import os
import subprocess
import paramiko

# Helper Classes

class SSH:
	def __init__(self, client: paramiko.SSHClient, certs_path: str, username: str, hostname: str):
		self.client = client
		self.certs_path = certs_path
		self.username = username
		self.hostname = hostname

# Folder Management

def create_r_u_dir(path:str, username:str, test=False) -> None:
	'''Creates ``root and user owned directory`` if it does not already exist.
	
	Args:
		path (str): Path to directory.
		username (str): Username.
		test (bool): Test mode status.

	Raises:
		IOError: Folder creation failed.
	'''
	if not os.path.isdir(path):
		print(f':: sudo install -d -m 0770 -o root -g {username} {path}')
		if not test:
			result = subprocess.run(['sudo', 'install', '-d', '-m', '0770', '-o', 'root', '-g', username, path],
									capture_output=True,
									text=True)
			if result.stderr != '': raise IOError(result.stderr)

def create_r_u_dir_ssh(ssh:SSH, path:str, test=False) -> None:
	'''Creates ``root and user owned directory on remote server`` if it does not already exist.
	
	Args:
		ssh (SSH): SSH object.
		path (str): Path to directory.
		test (bool): Test mode status.

	Raises:
		IOError: Folder creation failed.
	'''
	stdin, stdout, stderr = ssh.client.exec_command(f'[ -d {path} ]; echo $?'); stdin.close()
	# stdout contains $? != 0 if folder not exist; python interprets any number != 0 as True, therefore with double negation...
	dir_not_exist = bool(int(stdout.read().decode()))
	if dir_not_exist:
		print(f'(ssh) :: sudo install -d -m 0770 -o root -g {ssh.username} {ssh.username}@{ssh.hostname}:{path}')
		if not test:
			stdin, stdout, stderr = ssh.client.exec_command(f'sudo install -d -m 0770 -o root -g {ssh.username} {path}'); stdin.close()
			err = stderr.read().decode().strip()
			if err != '': raise IOError(err)

# SSH

def connect_ssh(ssh_path: str, ssh_certs_path: str) -> SSH | None:
	'''Creates and returns an SSH Object if path and certs are set.
	
	Args:
		ssh_path (str): Required path for valid SSH Client creation. If empty string, then no client is created.
		ssh_certs_path (str): Required path to SSH certificates.

	Returns:
		out (SSH): Valid and connected SSH client with username and hostname.

	Raises:
		SSHException: SSH connection could not be established.
	'''
	if ssh_path != '':
		if ssh_certs_path != '':
			ssh_username, ssh_hostname = ssh_path.split('@')
			ssh = paramiko.SSHClient()
			try:
				ssh_key = paramiko.Ed25519Key.from_private_key_file(ssh_certs_path)
			except:
				raise paramiko.SSHException('"ssh_certs" needs to point to a valid ed25519 encoded private key.')
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=ssh_hostname, username=ssh_username, pkey=ssh_key)
			print()
			print(f'Valid SSH connection @ {ssh_path}.')
			return SSH(ssh, ssh_certs_path, ssh_username, ssh_hostname)
		else:
			raise paramiko.SSHException('"ssh_certs" needs to be set.')
		
	return None