'''
	cpsnap_helper.py
	cpsnap helper functions

	Copyright © 2025 Hanozumi
'''

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