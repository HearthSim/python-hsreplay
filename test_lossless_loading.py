#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from datetime import datetime
from io import BytesIO
from hsreplay.document import HSReplayDocument


BUILD = 12345


def main():
	parser = ArgumentParser()
	parser.add_argument("files", nargs="*")
	args = parser.parse_args(sys.argv[1:])
	default_date = datetime.now()
	for filename in args.files:
		with open(filename) as f:
			doc_in = HSReplayDocument.from_log_file(f, date=default_date, build=BUILD)
			xml_in = doc_in.to_xml(pretty=True)
			xml_file_in = BytesIO(xml_in.encode("utf-8"))
			doc_out = HSReplayDocument.from_xml_file(xml_file_in)
			xml_out = doc_out.to_xml(pretty=True)
			assert 'build="%i"' % (BUILD) in xml_out, "Can't find build in output file!"

			if xml_in != xml_out:
				with open("in.xml", "w") as f, open("out.xml", "w") as f2:
					f.write(xml_in)
					f2.write(xml_out)
				raise Exception("%r: Log -> XML -> Document -> XML: FAIL" % (filename))
			else:
				print("%r: Log -> XML -> Document -> XML: SUCCESS" % (filename))

			packet_tree_in = doc_in.to_packet_tree()
			doc_out2 = HSReplayDocument.from_packet_tree(packet_tree_in, build=BUILD)
			xml_out2 = doc_out2.to_xml(pretty=True)

			if xml_in != xml_out2:
				with open("in.xml", "w") as f, open("out2.xml", "w") as f2:
					f.write(xml_in)
					f2.write(xml_out2)
				raise Exception("%r: Document -> PacketTree -> Document: FAIL" % (filename))
			else:
				print("%r: Document -> PacketTree -> Document: SUCCESS" % (filename))


if __name__ == "__main__":
	main()
