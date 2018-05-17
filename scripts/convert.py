#!/usr/bin/env python
import sys
from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime

from hsreplay.document import HSReplayDocument


def date_arg(s):
	try:
		return datetime.strptime(s, "%Y-%m-%d")
	except ValueError as e:
		raise ArgumentTypeError(e)


def main():
	parser = ArgumentParser()
	parser.add_argument("files", nargs="*")
	parser.add_argument("--processor", dest="processor", default="GameState")
	parser.add_argument("--default-date", dest="date", type=date_arg, help="Format: YYYY-MM-DD")
	# https://stackoverflow.com/questions/9226516/
	args = parser.parse_args(sys.argv[1:])
	for filename in args.files:
		with open(filename) as f:
			doc = HSReplayDocument.from_log_file(f, args.processor, args.date)
			print(doc.to_xml())


if __name__ == "__main__":
	main()
