#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from hsreplay import log_to_xml


def main():
	parser = ArgumentParser()
	parser.add_argument("files", nargs="*")
	parser.add_argument("--processor", dest="processor", default="GameState")
	args = parser.parse_args(sys.argv[1:])
	for filename in args.files:
		with open(filename) as f:
			print(log_to_xml(f, args.processor))


if __name__ == "__main__":
	main()
