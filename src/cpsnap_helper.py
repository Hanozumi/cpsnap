'''
	cpsnap_helper.py
	cpsnap helper functions

	Copyright © 2025 Hanozumi
'''

import os
import subprocess
import getpass

def query_y_n(query: str, yes_default=True) -> bool:
	'''Queries the user with a yes/no prompt.

	Args:
		query (str): The question prompting the users input.
		yes_default (bool): Sets whether yes or no are the default value.

	Returns:
		out (bool): True for yes and False for no.

	Raises:
		ValueError: An invalid default value has been set.
	'''
	
	valid = { 'yes': True, 'ye': True, 'y': True, 'n': False, 'no': False }
	if yes_default == None:
		prompt = ' [y/n] '
	elif yes_default == True:
		prompt = ' [Y/n] '
	elif yes_default == False:
		prompt = ' [y/N] '
	else:
		raise ValueError(f'The input "{yes_default}" is invalid. Can only be True, False, None.')
	
	while True:
		choice = input(query + prompt).lower()
		if yes_default != None and choice.strip() == '':
			return yes_default
		elif choice in valid:
			return valid[choice]
		else:
			print('Incorrect input. Try again.')

def ask_create_r_u_dir(path: str, query: str, test=False):
	'''Prompts user whether to create directory if it does not already exit.

	Args:
		path (str): Path to directory.
		query (str): The question prompting the users input.
		test (bool): Test mode status.
	'''
	query_result = query_y_n(query)
	if not os.path.isdir(path) and query_result:
		print(f':: sudo install -d -m 0770 -o root -g {getpass.getuser()} {path}')
		if not test:
			result = subprocess.run(['sudo', 'install', '-d', '-m', '0770', '-o', 'root', '-g', getpass.getuser(), path],
						   capture_output=True,
						   text=True)
			if result.stderr != '': print(result.stderr, end='')
	elif not query_result:
		print('\nDid not create backup folder.\n:: Exiting...')
		exit(255)

def create_r_u_dir(path:str, test=False):
	'''Creates directory if it does not already exist.
	
	Args:
		path (str): Path to directory.
		test (bool): Test mode status.
	'''
	print(f':: sudo install -d -m 0770 -o root -g {getpass.getuser()} {path}')
	if not test:
			result = subprocess.run(['sudo', 'install', '-d', '-m', '0770', '-o', 'root', '-g', getpass.getuser(), path],
						   capture_output=True,
						   text=True)
			if result.stderr != '': print(result.stderr, end='')