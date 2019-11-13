#!/usr/bin/env python
"""
A command line tool for annotating .hsreplay files with GameTag data to
facilitate development activities.
"""
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
	parser.add_argument(
		"outfile", nargs="?", help="the annotated replay data"
	)

	args = parser.parse_args()
	annotate_replay(args.infile, open(args.outfile, "wb"))


if __name__ == "__main__":
	main()
