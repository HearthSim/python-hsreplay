try:
	from lxml import etree as ElementTree
	LXML = True
except ImportError:
	from xml.etree import ElementTree
	LXML = False
try:
	from aniso8601 import parse_datetime
except ImportError:
	from dateutil.parser import parse as parse_datetime

import enum
from xml.dom import minidom

from . import SYSTEM_DTD

__all__ = [
	"ElementTree", "annotate_replay", "parse_datetime", "pretty_xml", "toxml"
]


def toxml(root, pretty):
	if LXML:
		kwargs = {
			"doctype": '<!DOCTYPE hsreplay SYSTEM "%s">' % (SYSTEM_DTD),
			"pretty_print": pretty,
			"xml_declaration": True,
			"encoding": "utf-8",
		}
		xml = ElementTree.tostring(root, **kwargs)
		return xml.decode("utf-8")

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


def _to_string(tag):
	result = "<%s" % tag.tag
	if len(tag.attrib):
		result += " "
		result += " ".join("%s=%s" % item for item in tag.attrib.items())
	result += ">"
	return result


class ResolvedString(str):
	is_resolved = True


def _get_card_name(db, card_id):
	if hasattr(card_id, "is_resolved") and card_id.is_resolved:
		return card_id
	if card_id not in db:
		return "Unknown card %s" % card_id
	return db[card_id].name


def annotate_replay(infile, outfile):
	from hearthstone import cardxml
	from hearthstone.enums import (
		TAG_TYPES, BlockType, GameTag, MetaDataType, PlayState, State
	)
	db, _ = cardxml.load()
	entities = {}

	entity_ref_tags = {
		GameTag.LAST_AFFECTED_BY,
		GameTag.LAST_CARD_PLAYED,
		GameTag.PROPOSED_ATTACKER,
		GameTag.PROPOSED_DEFENDER,
		GameTag.WEAPON,
	}

	tree = ElementTree.parse(infile)
	root = tree.getroot()

	for tag in root.iter("FullEntity"):
		if "cardID" in tag.attrib:
			entities[tag.attrib["id"]] = tag.attrib["cardID"]

	for tag in root.iter("GameEntity"):
		entities[tag.attrib["id"]] = ResolvedString("GameEntity")

	for tag in root.iter("Player"):
		if "name" in tag.attrib:
			entities[tag.attrib["id"]] = ResolvedString(tag.attrib["name"])

	for tag in root.iter("ShowEntity"):
		if "cardID" in tag.attrib:
			entities[tag.attrib["entity"]] = tag.attrib["cardID"]
			tag.set("EntityName", _get_card_name(db, tag.attrib["cardID"]))

	for tag in root.iter("FullEntity"):
		if tag.attrib["id"] in entities:
			tag.set("EntityName", _get_card_name(db, entities[tag.attrib["id"]]))

	block_counter = 1
	for tag in root.iter("Block"):
		tag.set("block_sequence_num", str(block_counter))
		block_counter += 1
		if "entity" in tag.attrib and tag.attrib["entity"] in entities:
			tag.set("EntityCardID", entities[tag.attrib["entity"]])
			if tag.attrib["entity"] == "1":
				tag.set("EntityCardName", "GameEntity")
			elif tag.attrib["entity"] in ("2", "3"):
				tag.set("EntityCardName", entities[tag.attrib["entity"]])
			else:
				tag.set("EntityCardName", _get_card_name(db, entities[tag.attrib["entity"]]))

		if "target" in tag.attrib and tag.attrib["target"] in entities:
			tag.set("TargetName", _get_card_name(db, entities[tag.attrib["target"]]))

		if "triggerKeyword" in tag.attrib:
			try:
				tag.set("TriggerKeywordName", GameTag(int(tag.attrib["triggerKeyword"])).name)
			except ValueError:
				pass

	for tag in root.iter("Tag"):
		try:
			tag_enum = GameTag(int(tag.attrib["tag"]))
			tag.set("GameTagName", tag_enum.name)

			enum_or_type = TAG_TYPES.get(tag_enum)
			if enum_or_type:
				if enum_or_type.__class__ == enum.EnumMeta:
					tag.set(
						"%sName" % (enum_or_type.__name__),
						enum_or_type(int(tag.attrib["value"])).name
					)
		except ValueError:
			pass

	for tag_change in root.iter("TagChange"):
		if "entity" in tag_change.attrib and tag_change.attrib["entity"] in entities:
			tag_change.set("EntityCardID", entities[tag_change.attrib["entity"]])
			tag_change.set("EntityCardName", _get_card_name(db, entities[tag_change.attrib["entity"]]))

		if int(tag_change.attrib["tag"]) in entity_ref_tags and tag_change.attrib["value"] in entities:
			tag_change.set("ValueReferenceCardID", entities[tag_change.attrib["value"]])
			tag_change.set(
				"ValueReferenceCardName",
				_get_card_name(db, entities[tag_change.attrib["value"]])
			)

		if tag_change.attrib["tag"] == str(GameTag.STATE.value):
			tag_change.set("StateName", State(int(tag_change.attrib["value"])).name)

		if tag_change.attrib["tag"] == str(GameTag.PLAYSTATE.value):
			tag_change.set("PlayStateName", PlayState(int(tag_change.attrib["value"])).name)

		try:
			tag_enum = GameTag(int(tag_change.attrib["tag"]))
			tag_change.set("GameTagName", tag_enum.name)

			enum_or_type = TAG_TYPES.get(tag_enum)
			if enum_or_type:
				if enum_or_type.__class__ == enum.EnumMeta:
					tag_change.set(
						"%sName" % (enum_or_type.__name__),
						enum_or_type(int(tag_change.attrib["value"])).name
					)
		except ValueError:
			pass

	for block in root.iter("Block"):
		try:
			tag_enum = BlockType(int(block.attrib["type"]))
		except ValueError:
			tag_enum = block.attrib["type"]

		block.set("BlockTypeName", tag_enum.name)

	for option in root.iter("Option"):
		if "entity" in option.attrib and option.attrib["entity"] in entities:
			option.set("EntityCardID", entities[option.attrib["entity"]])
			option.set("EntityName", _get_card_name(db, entities[option.attrib["entity"]]))

	for target in root.iter("Target"):
		if "entity" in target.attrib and target.attrib["entity"] in entities:
			target.set("EntityCardID", entities[target.attrib["entity"]])
			target.set("EntityName", _get_card_name(db, entities[target.attrib["entity"]]))

	for choices in root.iter("Choices"):
		if "entity" in choices.attrib and choices.attrib["entity"] in entities:
			choices.set("EntityCardID", entities[choices.attrib["entity"]])
			choices.set("EntityName", _get_card_name(db, entities[choices.attrib["entity"]]))
		if "source" in choices.attrib and choices.attrib["source"] in entities:
			choices.set("SourceCardID", entities[choices.attrib["source"]])
			choices.set("SourceName", _get_card_name(db, entities[choices.attrib["source"]]))

	for choice in root.iter("Choice"):
		if "entity" in choice.attrib and choice.attrib["entity"] in entities:
			choice.set("EntityCardID", entities[choice.attrib["entity"]])
			choice.set("EntityName", _get_card_name(db, entities[choice.attrib["entity"]]))

	for meta in root.iter("MetaData"):
		if "meta" in meta.attrib:
			meta.set("MetaName", MetaDataType(int(meta.attrib["meta"])).name)

	for target in root.iter("Info"):
		if "entity" in target.attrib and target.attrib["entity"] in entities:
			target.set("EntityName", _get_card_name(db, entities[target.attrib["entity"]]))

	tree.write(outfile, pretty_print=True)


def set_game_meta_on_game(game_meta, game_element):
	if game_meta is None:
		return

	if game_meta.get("id") is not None:
		game_element._attributes["id"] = str(game_meta["id"])
	if game_meta.get("format") is not None:
		game_element._attributes["format"] = str(game_meta["format"])
	if game_meta.get("hs_game_type") is not None:
		game_element._attributes["type"] = str(game_meta["hs_game_type"])
	if game_meta.get("scenario_id") is not None:
		game_element._attributes["scenarioID"] = str(game_meta["scenario_id"])

	if "reconnecting" in game_meta:
		game_element._attributes["reconnecting"] = str(game_meta["reconnecting"])
