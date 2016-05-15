try:
	from lxml import etree as ElementTree
	LXML = True
except ImportError:
	from xml.etree import ElementTree
	LXML = False
from xml.dom import minidom
from . import SYSTEM_DTD


def toxml(root, pretty):
	if LXML:
		doctype = '<!DOCTYPE hsreplay SYSTEM "%s">' % (SYSTEM_DTD)
		xml = ElementTree.tostring(root, doctype=doctype, pretty_print=pretty)
		return xml.decode("utf-8")

	xml = ElementTree.tostring(root)

	if pretty:
		return pretty_xml(root)
	return ElementTree.tostring(root).decode("utf-8")


def pretty_xml(root):
	xml = ElementTree.tostring(root)
	ret = minidom.parseString(xml)

	imp = minidom.DOMImplementation()
	doctype = imp.createDocumentType(
		qualifiedName="hsreplay",
		publicId="",
		systemId=SYSTEM_DTD,
	)
	doc = imp.createDocument(None, "HSReplay", doctype)
	for element in list(ret.documentElement.childNodes):
		doc.documentElement.appendChild(element)
	for k, v in root.attrib.items():
		doc.documentElement.setAttribute(k, v)

	ret = doc.toprettyxml(indent="\t")
	return "\n".join(line for line in ret.split("\n") if line.strip())
