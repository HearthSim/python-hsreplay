#!/usr/bin/env python
"""
A command line tool for annotating .hsreplay files with GameTag data to
facilitate development activities.
"""
import os
import sys
from argparse import ArgumentParser, ArgumentTypeError, FileType
from datetime import datetime

from hsreplay.utils import annotate_replay


def date_arg(s):
	try:
		return datetime.strptime(s, "%Y-%m-%d")
	except ValueError as e:
		raise ArgumentTypeError(e)


def main():
	parser = ArgumentParser(description=__doc__)
	parser.add_argument(
		"infile", nargs="?", type=FileType("r"), default=sys.stdin,
		help="the input replay data"
	)

	args = parser.parse_args()
	with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as outfile:
		annotate_replay(args.infile, outfile)


if __name__ == "__main__":
	main()
