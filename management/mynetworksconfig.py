#!/usr/local/lib/mailinabox/env/bin/python

# NOTE:
# This script is run both using the system-wide Python 3
# interpreter (/usr/bin/python3) as well as through the
# virtualenv (/usr/local/lib/mailinabox/env). So only
# import packages at the top level of this script that
# are installed in *both* contexts. 

import pprint
import utils

from mailconfig import open_database

def get_mynetworks(env):
	c = open_database(env)
	c.execute('SELECT * FROM mynetworks')
	mynetworks = [ ';'.join(row) for row in c.fetchall() ]
	return mynetworks

if __name__ == "__main__":
	import sys

	if len(sys.argv) > 1 and sys.argv[1] == "list":
		from utils import load_environment
		pprint(get_mynetworks(utils.load_environment()))
