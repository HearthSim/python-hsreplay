from xml.dom import minidom
from xml.etree import ElementTree
from . import SYSTEM_DTD


def pretty_xml(xml):
	ret = ElementTree.tostring(xml)
	ret = minidom.parseString(ret)

	imp = minidom.DOMImplementation()
	doctype = imp.createDocumentType(
		qualifiedName="hsreplay",
		publicId="",
		systemId=SYSTEM_DTD,
	)
	doc = imp.createDocument(None, "HSReplay", doctype)
	for element in list(ret.documentElement.childNodes):
		doc.documentElement.appendChild(element)
	for k, v in xml.attrib.items():
		doc.documentElement.setAttribute(k, v)

	ret = doc.toprettyxml(indent="\t")
	return "\n".join(line for line in ret.split("\n") if line.strip())
