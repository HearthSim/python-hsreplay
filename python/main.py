#!/usr/bin/env python
import re
import sys
from hearthstone import enums, hslog
from hearthstone.enums import GameTag
from xml.etree import ElementTree
from xml.dom import minidom


__version__ = "1.0"

SYSTEM_DTD = "http://hearthsim.info/hsreplay/dtd/hsreplay-%s.dtd" % (__version__)


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

	ret = doc.toprettyxml(indent="\t")
	return "\n".join(line for line in ret.split("\n") if line.strip())


class Node:
	attributes = ()

	def __init__(self, *args):
		self.nodes = []
		for k, arg in zip(("ts", ) + self.attributes, args):
			setattr(self, k, arg)

	def append(self, node):
		self.nodes.append(node)

	def xml(self):
		element = ElementTree.Element(self.tagname)
		for node in self.nodes:
			element.append(node.xml())
		for attr in self.attributes:
			attrib = getattr(self, attr)
			if isinstance(attrib, int):
				# Check for enums
				attrib = str(int(attrib))
			if attrib is not None:
				element.attrib[attr] = attrib
		if self.timestamp and self.ts:
			element.attrib["ts"] = self.ts
		return element

	def __repr__(self):
		return "<%s>" % (self.__class__.__name__)


class GameNode(Node):
	tagname = "Game"
	timestamp = True

	def __init__(self, ts):
		super().__init__(ts)
		self.first_player = None
		self.second_player = None


class GameEntityNode(Node):
	tagname = "GameEntity"
	attributes = ("id", )
	timestamp = False


class PlayerNode(Node):
	tagname = "Player"
	attributes = ("id", "playerID", "accountHi", "accountLo", "name")
	timestamp = False


class FullEntityNode(Node):
	tagname = "FullEntity"
	attributes = ("id", "cardID")
	timestamp = False


class ShowEntityNode(Node):
	tagname = "ShowEntity"
	attributes = ("entity", "cardID")
	timestamp = False


class ActionNode(Node):
	tagname = "Action"
	attributes = ("entity", "type", "index", "target")
	timestamp = True


class MetaDataNode(Node):
	tagname = "MetaData"
	attributes = ("meta", "entity", "info")
	timestamp = False


class MetaDataInfoNode(Node):
	tagname = "Info"
	attributes = ("index", "entity")
	timestamp = False


class TagNode(Node):
	tagname = "Tag"
	attributes = ("tag", "value")
	timestamp = False


class TagChangeNode(Node):
	tagname = "TagChange"
	attributes = ("entity", "tag", "value")
	timestamp = False


class HideEntityNode(Node):
	tagname = "HideEntity"
	attributes = ("entity", "zone")
	timestamp = True


##
# Choices

class ChoicesNode(Node):
	tagname = "Choices"
	attributes = ("entity", "id", "taskList", "type", "min", "max", "source")
	timestamp = True


class ChoiceNode(Node):
	tagname = "Choice"
	attributes = ("index", "entity")
	timestamp = False


class ChosenEntitiesNode(Node):
	tagname = "ChosenEntities"
	attributes = ("entity", "id")
	timestamp = True


class SendChoicesNode(Node):
	tagname = "SendChoices"
	attributes = ("id", "type")
	timestamp = True


##
# Options

class OptionsNode(Node):
	tagname = "Options"
	attributes = ("id", )
	timestamp = True


class OptionNode(Node):
	tagname = "Option"
	attributes = ("index", "entity", "type")
	timestamp = False


class SubOptionNode(Node):
	tagname = "SubOption"
	attributes = ("index", "entity")
	timestamp = False


class OptionTargetNode(Node):
	tagname = "Target"
	attributes = ("index", "entity")
	timestamp = False


class SendOptionNode(Node):
	tagname = "SendOption"
	attributes = ("option", "subOption", "target", "position")
	timestamp = False


def add_initial_tags(ts, packet, packet_element):
	for tag, value in packet.tags:
		tag_element = TagNode(ts, tag, value)
		packet_element.append(tag_element)


def add_choices(ts, packet, packet_element):
	for i, choice in enumerate(packet.choices):
		choice_element = ChoiceNode(ts, i, choice.id)
		packet_element.append(choice_element)


def add_options(ts, packet, packet_element):
	for i, option in enumerate(packet.options):
		if option.optype == "option":
			cls = OptionNode
		elif option.optype == "target":
			cls = OptionTargetNode
		elif option.optype == "subOption":
			cls = SubOptionNode
		else:
			raise NotImplementedError("Unhandled option type: %r" % (option.optype))
		entity = option.entity.id if option.entity else None
		option_element = cls(ts, i, entity, option.type)
		add_options(ts, option, option_element)
		packet_element.append(option_element)


def add_packets_recursive(entity, entity_element):
	for packet in entity:
		_ent = packet.entity.id if packet.entity else None
		ts = packet.ts

		if isinstance(packet, hslog.packets.CreateGame):
			packet_element = GameEntityNode(ts, _ent)
			add_initial_tags(ts, packet, packet_element)
			entity_element.append(packet_element)
			for player in packet.players:
				player_element = PlayerNode(
					ts, player.entity, player.playerid,
					player.hi, player.lo, player.name
				)
				entity_element.append(player_element)
				add_initial_tags(ts, player, player_element)
			continue
		elif isinstance(packet, hslog.packets.Action):
			packet_element = ActionNode(
				ts, _ent, packet.type,
				packet.index if packet.index != -1 else None,
				packet.target.id if packet.target else None
			)
			add_packets_recursive(packet, packet_element)
		elif isinstance(packet, hslog.packets.ActionMetaData):
			# With verbose=false, we always have 0 packet.info :(
			assert len(packet.info) in (0, packet.count)
			packet_element = MetaDataNode(
				ts, packet.type, _ent, packet.count
			)
			for i, info in enumerate(packet.info):
				e = MetaDataInfoNode(packet.ts, i, info.id)
				packet_element.append(e)
		elif isinstance(packet, hslog.packets.TagChange):
			packet_element = TagChangeNode(
				packet.ts, _ent, packet.tag, packet.value
			)
		elif isinstance(packet, hslog.packets.HideEntity):
			packet_element = HideEntityNode(ts, _ent, packet.zone)
		elif isinstance(packet, hslog.packets.ShowEntity):
			packet_element = ShowEntityNode(ts, _ent, packet.cardid)
			add_initial_tags(ts, packet, packet_element)
		elif isinstance(packet, hslog.packets.FullEntity):
			packet_element = FullEntityNode(ts, _ent, packet.cardid)
			add_initial_tags(ts, packet, packet_element)
		elif isinstance(packet, hslog.packets.Choices):
			packet_element = ChoicesNode(
				ts, _ent, packet.id, packet.tasklist, packet.type,
				packet.min, packet.max, packet.source.id
			)
			add_choices(ts, packet, packet_element)
		elif isinstance(packet, hslog.packets.SendChoices):
			packet_element = SendChoicesNode(ts, packet.id, packet.type)
			add_choices(ts, packet, packet_element)
		elif isinstance(packet, hslog.packets.ChosenEntities):
			packet_element = ChosenEntitiesNode(ts, _ent, packet.id)
			add_choices(ts, packet, packet_element)
		elif isinstance(packet, hslog.packets.Options):
			packet_element = OptionsNode(ts, packet.id)
			add_options(ts, packet, packet_element)
		elif isinstance(packet, hslog.packets.SendOption):
			packet_element = SendOptionNode(
				ts, packet.option, packet.suboption, packet.target, packet.position
			)
		else:
			raise NotImplementedError(repr(packet))
		entity_element.append(packet_element)


def main():
	fname = sys.argv[1]
	parser = hslog.LogWatcher()

	with open(fname, "r") as f:
		parser.read(f)

	builder = ElementTree.TreeBuilder()
	builder.start("HSReplay", {"version": __version__})
	builder.end("HSReplay")
	root = builder.close()

	for game in parser.games:
		game_element = GameNode(game.ts)

		add_packets_recursive(game, game_element)

		root.append(game_element.xml())

	print(pretty_xml(root))


if __name__ == "__main__":
	main()
