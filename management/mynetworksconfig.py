#!/usr/local/lib/mailinabox/env/bin/python

# NOTE:
# This script is run both using the system-wide Python 3
# interpreter (/usr/bin/python3) as well as through the
# virtualenv (/usr/local/lib/mailinabox/env). So only
# import packages at the top level of this script that
# are installed in *both* contexts. 

import argparse
import json
import sqlite3
import sys

from pprint import pprint

import utils


def open_database(env, with_connection=False):
	conn = sqlite3.connect(env["STORAGE_ROOT"] + "/mynetworks.sqlite")
	if not with_connection:
		return conn.cursor()
	else:
		return conn, conn.cursor()


def get_mynetworks(env):
	c = open_database(env)
	c.row_factory = sqlite3.Row
	c.execute('SELECT * FROM mynetworks')
	mynetworks = []
	for row in c.fetchall():
		mynetworks.append({item: row[item] for item in row.keys()})
	return mynetworks


def list_func(args):
	from utils import load_environment

	mynetworks = get_mynetworks(utils.load_environment())

	if args.json:
		json.dump(mynetworks, sys.stdout)
	elif args.cidr:
		cidrs = {item['cidr']: item['description'] for item in mynetworks}
		json.dump(cidrs, sys.stdout)
	else:
		pprint(mynetworks)


def argparser():
	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()

	list_parser = subparsers.add_parser('list', help='mynetworks database content')
	list_parser.add_argument('-j', '--json', action='store_true', help='output in JSON format')
	list_parser.add_argument('-c', '--cidr', action='store_true', help='output in JSON format, but unique CIRDs and descriptions')
	list_parser.set_defaults(func=list_func)

	return parser


if __name__ == "__main__":

	args = argparser().parse_args()
	args.func(args)	
