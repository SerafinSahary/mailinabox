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

from ipaddress import ip_network, ip_address, AddressValueError, NetmaskValueError
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
	c.execute('SELECT * FROM mynetworks ORDER BY cidr, id')
	mynetworks = []
	for row in c.fetchall():
		mynetworks.append({item: row[item] for item in row.keys()})
	return mynetworks


def validate_cidr(cidr: str):
	try:
		ip_network(cidr, strict=True)
	except (AddressValueError, NetmaskValueError, ValueError) as ex:
		return False
	
	return True


def add_mynetwork(env, cidr, description):
	if not validate_cidr(cidr):
		raise ValueError

	conn, c = open_database(env, with_connection=True)
	c.execute('SELECT DISTINCT cidr FROM mynetworks')

	mynetwork_to_add = ip_network(cidr, strict=True)
	
	for item in c.fetchall():
		if mynetwork_to_add.overlaps(ip_network(item[0])) or \
		   ip_network(item[0]).overlaps(mynetwork_to_add):
			raise ValueError
	
	records_to_add = [(cidr, str(item), description) for item in mynetwork_to_add.hosts()]

	c.executemany(
		'INSERT INTO mynetworks(cidr, addr_in_range, description) VALUES(?, ?, ?)',
		records_to_add
	)

	conn.commit()


def remove_mynetwork(env, cidr):
	if not validate_cidr(cidr):
		raise ValueError

	conn, c = open_database(env, with_connection=True)
	c.execute('DELETE FROM mynetworks WHERE cidr = ?', (cidr, ))
	conn.commit()


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


def add_func(args):
	from utils import load_environment

	add_mynetwork(utils.load_environment(), args.cidr, args.descr)


def remove_func(args):
	from utils import load_environment

	remove_mynetwork(utils.load_environment(), args.cidr)


def argparser():
	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()

	list_parser = subparsers.add_parser('list', help='mynetworks database content')
	list_parser.add_argument('-j', '--json', action='store_true', help='output in JSON format')
	list_parser.add_argument('-c', '--cidr', action='store_true', help='output in JSON format, but unique CIRDs and descriptions')
	list_parser.set_defaults(func=list_func)

	add_parser = subparsers.add_parser('add', help='add mynetworks entry')
	add_parser.add_argument('cidr', help='cidr address of the network to add')
	add_parser.add_argument('descr', help='description of the network to add')
	add_parser.set_defaults(func=add_func)

	remove_parser = subparsers.add_parser('remove', help='remove mynetworks entry')
	remove_parser.add_argument('cidr', help='cidr address of the network to remove')
	remove_parser.set_defaults(func=remove_func)

	return parser


if __name__ == "__main__":
	args = argparser().parse_args()
	if hasattr(args, 'func'):
		args.func(args)
