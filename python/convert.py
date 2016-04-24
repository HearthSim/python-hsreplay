#!/usr/bin/env python
import sys
import codecs
from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
from hsreplay.dumper import log_to_xml
from os import path
from os.path import basename


def date_arg(s):
	try:
		return datetime.strptime(s, "%Y-%m-%d")
	except ValueError as e:
		raise ArgumentTypeError(e) from e


def main():
	parser = ArgumentParser()
	parser.add_argument("files", nargs="*")
	parser.add_argument("--processor", dest="processor", default="GameState")
	parser.add_argument("--default-date", dest="date", type=date_arg, help="Format: YYYY-MM-DD")
	# https://stackoverflow.com/questions/9226516/
	sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
	args = parser.parse_args(sys.argv[1:])
	for filename in args.files:
		with open(filename, encoding="utf-8") as f:
			out = open(path.splitext(basename(filename))[0] + ".hsreplay",'w', encoding="utf-8")
			print(log_to_xml(f, args.processor, args.date),file=out)


if __name__ == "__main__":
	main()
