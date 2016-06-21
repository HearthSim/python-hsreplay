#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from datetime import datetime
from io import StringIO
from hsreplay.document import HSReplayDocument


def main():
	parser = ArgumentParser()
	parser.add_argument("files", nargs="*")
	args = parser.parse_args(sys.argv[1:])
	default_date = datetime.now()
	for filename in args.files:
		with open(filename) as f:
			doc_in = HSReplayDocument.from_log_file(f, date=default_date)
			xml_in = doc_in.to_xml()
			xml_file_in = StringIO(xml_in)
			doc_out = HSReplayDocument.from_xml_file(xml_file_in)
			xml_out = doc_out.to_xml()

			with open("in.xml", "w") as f:
				f.write(xml_in)

			with open("out.xml", "w") as f:
				f.write(xml_out)

			assert xml_in == xml_out
			print("OK!")


if __name__ == "__main__":
	main()
