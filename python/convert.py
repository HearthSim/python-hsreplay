#!/usr/bin/env python
import sys
from hsreplay import log_to_xml


def main():
	filename = sys.argv[1]
	with open(filename) as f:
		print(log_to_xml(f))


if __name__ == "__main__":
	main()
