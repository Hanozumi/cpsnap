'''
	cpsnap_name_funcs.py
	naming function definitions for cpsnap backups

	Copyright © 2025 Hanozumi
'''

from datetime import datetime

name_funcs = {
	'none':		lambda: '',
	'date':		lambda:	datetime.now().strftime('%Y-%m-%d'),
	'datetime':	lambda:	datetime.now().strftime('%Y-%m-%d-%H_%M'),
	'weekday':	lambda:	datetime.now().strftime('%Y-%m-%d_%A')
}