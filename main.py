#!/usr/bin/env python
import re
import sys
from xml.etree import ElementTree
from xml.dom import minidom


POWERLOG_LINE_RE = re.compile(r"^D ([\d:.]+) ([^(]+)\(\) - (.+)$")
OUTPUTLOG_LINE_RE = re.compile(r"\[Power\] ()([^(]+)\(\) - (.+)$")

ENTITY_RE = re.compile("\[.*\s*id=(\d+)\s*.*\]")

CHOICES_CHOICE_RE = re.compile(r"id=(\d+) PlayerId=(\d+) ChoiceType=(\w+) CountMin=(\d+) CountMax=(\d+)$")
CHOICES_SOURCE_RE = re.compile(r"Source=(\[?.+\]?)$")
CHOICES_ENTITIES_RE = re.compile(r"Entities\[(\d+)\]=(\[.+\])$")

SEND_CHOICES_CHOICETYPE_RE = re.compile(r"id=(\d+) ChoiceType=(.+)$")
SEND_CHOICES_ENTITIES_RE = re.compile(r"m_chosenEntities\[(\d+)\]=(\[.+\])$")

OPTIONS_ENTITY_RE = re.compile(r"id=(\d+)$")
OPTIONS_OPTION_RE = re.compile(r"option (\d+) type=(\w+) mainEntity=(.*)$")
OPTIONS_SUBOPTION_RE = re.compile(r"(subOption|target) (\d+) entity=(.*)$")

SEND_OPTION_RE = re.compile(r"selectedOption=(\d+) selectedSubOption=(-1|\d+) selectedTarget=(\d+) selectedPosition=(\d+)")

ACTION_TAG_RE = re.compile(r"tag=(\w+) value=(\w+)")
ACTION_FULLENTITY_RE_1 = re.compile(r"FULL_ENTITY - Updating (\[.+\]) CardID=(\w+)?$")
ACTION_FULLENTITY_RE_2 = re.compile(r"FULL_ENTITY - Creating ID=(\d+) CardID=(\w+)?$")
ACTION_SHOWENTITY_RE = re.compile(r"SHOW_ENTITY - Updating Entity=(\[?.+\]?) CardID=(\w+)$")
ACTION_HIDEENTITY_RE = re.compile(r"HIDE_ENTITY - Entity=(\[.+\]) tag=(\w+) value=(\w+)")
ACTION_TAGCHANGE_RE = re.compile(r"TAG_CHANGE Entity=(\[?.+\]?) tag=(\w+) value=(\w+)")
ACTION_START_RE = re.compile(r"ACTION_START Entity=(\[?.+\]?) (?:SubType|BlockType)=(\w+) Index=(-1|\d+) Target=(\[?.+\]?)$")
ACTION_METADATA_RE = re.compile(r"META_DATA - Meta=(\w+) Data=(\[?.+\]?) Info=(\d+)")
ACTION_CREATEGAME_RE = re.compile(r"GameEntity EntityID=(\d+)")
ACTION_CREATEGAME_PLAYER_RE = re.compile(r"Player EntityID=(\d+) PlayerID=(\d+) GameAccountId=\[hi=(\d+) lo=(\d+)\]$")


def pretty_xml(xml):
	ret = ElementTree.tostring(xml)
	ret = minidom.parseString(ret).toprettyxml(indent="\t")
	return "\n".join(line for line in ret.split("\n") if line.strip())


class Node:
	attributes = ["ts"]

	def __init__(self, ts):
		self.ts = ts
		self.nodes = []

	def append(self, node):
		self.nodes.append(node)

	def xml(self):
		element = ElementTree.Element(self.tagname)
		for node in self.nodes:
			element.append(node.xml())
		for attr in self.attributes:
			attrib = getattr(self, attr)
			if attrib:
				element.attrib[attr] = attrib
		return element

	def __repr__(self):
		return "<%s>" % (self.__class__.__name__)


class GameNode(Node):
	tagname = "Game"


class EntityDefNode(Node):
	def __init__(self, ts, id, cardID=None):
		super().__init__(ts)
		self.id = id
		self.cardID = cardID


class GameEntityNode(EntityDefNode):
	tagname = "GameEntity"
	attributes = ("id", )


class PlayerNode(EntityDefNode):
	tagname = "Player"
	attributes = ("id", "playerID", "name", "accountHi", "accountLo")


class FullEntityNode(EntityDefNode):
	tagname = "FullEntity"
	attributes = ("id", "cardID")


class ShowEntityNode(Node):
	tagname = "ShowEntity"
	attributes = ("entity", "cardID")

	def __init__(self, ts, entity, cardID):
		super().__init__(ts)
		self.entity = entity
		self.cardID = cardID


class ActionNode(Node):
	tagname = "Action"
	attributes = ("ts", "entity", "type", "index", "target")

	def __init__(self, ts, entity, type, index, target):
		super().__init__(ts)
		self.entity = entity
		self.type = type
		self.index = index
		self.target = target


class MetaDataNode(Node):
	tagname = "MetaData"
	attributes = ("meta", "data", "info")

	def __init__(self, ts, meta, data, info):
		super().__init__(ts)
		self.meta = meta
		self.data = data
		self.info = info


class TagNode(Node):
	tagname = "Tag"
	attributes = ("tag", "value")

	def __init__(self, tag, value):
		self.tag = tag
		self.value = value
		super().__init__(None)


class TagChangeNode(Node):
	tagname = "TagChange"
	attributes = ("entity", "tag", "value")

	def __init__(self, ts, entity, tag, value):
		super().__init__(ts)
		self.entity = entity
		self.tag = tag
		self.value = value


class HideEntityNode(Node):
	tagname = "HideEntity"
	attributes = ("ts", "entity", "tag", "value")

	def __init__(self, ts, entity, tag, value):
		super().__init__(ts)
		self.entity = entity
		self.tag = tag
		self.value = value


##
# Choices

class ChoicesNode(Node):
	tagname = "Choices"
	attributes = ("ts", "entity", "playerID", "type", "min", "max", "source")

	def __init__(self, ts, entity, playerID, type, min, max):
		super().__init__(ts)
		self.entity = entity
		self.playerID = playerID
		self.type = type
		self.min = min
		self.max = max
		self.source = "UNKNOWN"


class ChoiceNode(Node):
	tagname = "Choice"
	attributes = ("index", "entity")

	def __init__(self, index, entity):
		super().__init__(None)
		self.index = index
		self.entity = entity


class SendChoicesNode(Node):
	tagname = "SendChoices"
	attributes = ("ts", "entity", "type")

	def __init__(self, ts, entity, type):
		super().__init__(ts)
		self.entity = entity
		self.type = type


##
# Options

class OptionsNode(Node):
	attributes = ("ts", "id")
	tagname = "Options"

	def __init__(self, ts, id):
		super().__init__(ts)
		self.id = id


class OptionNode(Node):
	attributes = ("index", "type", "entity")
	tagname = "Option"

	def __init__(self, index, type, entity):
		super().__init__(None)
		self.index = index
		self.type = type
		self.entity = entity


class SubOptionNode(Node):
	attributes = ("index", "entity")
	tagname = "SubOption"

	def __init__(self, index, entity):
		super().__init__(None)
		self.index = index
		self.entity = entity


class OptionTargetNode(Node):
	attributes = ("index", "entity")
	tagname = "Target"

	def __init__(self, index, entity):
		super().__init__(None)
		self.index = index
		self.entity = entity


class SendOptionNode(Node):
	attributes = ("option", "subOption", "target", "position")
	tagname = "SendOption"

	def __init__(self, ts, option, subOption, target, position):
		super().__init__(ts)
		self.option = option
		self.subOption = subOption
		self.target = target
		self.position = position


class PlayerID:
	def __init__(self, game, data):
		self.game = game
		self.data = data

	def __contains__(self, other):
		return str(self).__contains__(other)

	def __str__(self):
		return self.game.players.get(self.data, "UNKNOWN PLAYER: %r" % (self.data))


class PowerLogParser:
	def __init__(self):
		self.ast = []

	def _parse_entity(self, data):
		if not data:
			return None
		sre = ENTITY_RE.match(data)
		if sre:
			id = sre.groups()[0]
			return id

		if data == "0":
			return None

		if data == "GameEntity":
			return self.game.id

		if data.isdigit():
			return data

		return self.game.players.get(data, PlayerID(self.game, data))

	def read(self, f):
		regex = None
		for line in f.readlines():
			if regex is None:
				sre = POWERLOG_LINE_RE.match(line)
				if sre:
					regex = POWERLOG_LINE_RE
				else:
					sre = OUTPUTLOG_LINE_RE.match(line)
					if sre:
						regex = OUTPUTLOG_LINE_RE
			else:
				sre = regex.match(line)

			if not sre:
				continue

			self.add_data(*sre.groups())

	def register_player_id(self, entity, id):
		# Power.log sucks, the entity IDs for players are not reliable.
		# We convert them to actual entity IDs...
		self.game.players[entity] = id
		self.game.playernodes[id].name = entity

	def add_data(self, ts, method, data):
		# if method == "PowerTaskList.DebugPrintPower":
		if method == "GameState.DebugPrintPower":
			self.handle_data(ts, data)
		elif method == "GameState.SendChoices":
			self.handle_send_choices(ts, data)
		elif method == "GameState.DebugPrintChoices":
			self.handle_choices(ts, data)
		elif method == "GameState.DebugPrintOptions":
			self.handle_options(ts, data)
		elif method == "GameState.SendOption":
			self.handle_send_option(ts, data)

	def handle_send_choices(self, ts, data):
		data = data.lstrip()

		sre = SEND_CHOICES_CHOICETYPE_RE.match(data)
		if sre:
			id, type = sre.groups()
			node = SendChoicesNode(ts, id, type)
			self.current_node.append(node)
			self.current_send_choice_node = node
			return

		sre = SEND_CHOICES_ENTITIES_RE.match(data)
		if sre:
			index, entity = sre.groups()
			entity = self._parse_entity(entity)
			node = ChoiceNode(index, entity)
			self.current_send_choice_node.append(node)
			return

		sys.stderr.write("Warning: Unhandled sent choices: %r\n" % (data))

	def handle_choices(self, ts, data):
		data = data.lstrip()

		sre = CHOICES_CHOICE_RE.match(data)
		if sre:
			entity, playerID, type, min, max = sre.groups()
			node = ChoicesNode(ts, entity, playerID, type, min, max)
			self.current_node.append(node)
			self.current_choice_node = node
			return

		sre = CHOICES_SOURCE_RE.match(data)
		if sre:
			entity, = sre.groups()
			entity = self._parse_entity(entity)
			self.current_choice_node.source = entity
			return

		sre = CHOICES_ENTITIES_RE.match(data)
		if sre:
			index, entity = sre.groups()
			entity = self._parse_entity(entity)
			node = ChoiceNode(index, entity)
			self.current_choice_node.append(node)

	def handle_data(self, ts, data):
		# print(data)
		stripped_data = data.lstrip()
		indent_level = len(data) - len(stripped_data)
		data = stripped_data

		sre = ACTION_TAG_RE.match(data)
		if sre:
			tag, value = sre.groups()
			node = TagNode(tag, value)
			assert self.entity_def
			self.entity_def.append(node)
			return

		sre = ACTION_TAGCHANGE_RE.match(data)
		if sre:
			self.entity_def = None
			entity, tag, value = sre.groups()
			if tag == "ENTITY_ID" and not entity.isdigit() and entity != "GameEntity":
				self.register_player_id(entity, value)
			entity = self._parse_entity(entity)
			node = TagChangeNode(ts, entity, tag, value)

			if self.current_node.indent_level > indent_level:
				# mismatched indent levels - closing the node
				# this can happen eg. during mulligans
				self.current_node = self.current_node.parent
			self.current_node.append(node)
			self.current_node.indent_level = indent_level
			return

		sre = ACTION_FULLENTITY_RE_1.match(data)
		if not sre:
			sre = ACTION_FULLENTITY_RE_2.match(data)
		if sre:
			entity, cardid = sre.groups()
			entity = self._parse_entity(entity)
			node = FullEntityNode(ts, entity, cardid)
			self.entity_def = node
			self.current_node.append(node)
			return

		sre = ACTION_SHOWENTITY_RE.match(data)
		if sre:
			entity, cardid = sre.groups()
			entity = self._parse_entity(entity)
			node = ShowEntityNode(ts, entity, cardid)
			self.entity_def = node
			self.current_node.append(node)
			return

		sre = ACTION_HIDEENTITY_RE.match(data)
		if sre:
			entity, tag, value = sre.groups()
			entity = self._parse_entity(entity)
			node = HideEntityNode(ts, entity, tag, value)
			self.current_node.append(node)
			return

		sre = ACTION_START_RE.match(data)
		if sre:
			entity, type, index, target = sre.groups()
			entity = self._parse_entity(entity)
			target = self._parse_entity(target)
			node = ActionNode(ts, entity, type, index, target)
			self.current_node.append(node)
			node.parent = self.current_node
			self.current_node = node
			self.current_node.indent_level = indent_level
			return

		sre = ACTION_METADATA_RE.match(data)
		if sre:
			meta, data, info = sre.groups()
			data = self._parse_entity(data)
			node = MetaDataNode(ts, meta, data, info)
			self.current_node.append(node)
			return

		sre = ACTION_CREATEGAME_RE.match(data)
		if sre:
			id, = sre.groups()
			assert id == "1"
			self.game.id = id
			node = GameEntityNode(ts, id)
			self.current_node.append(node)
			self.entity_def = node
			return

		sre = ACTION_CREATEGAME_PLAYER_RE.match(data)
		if sre:
			id, playerID, accountHi, accountLo = sre.groups()
			node = PlayerNode(ts, id)
			node.playerID = playerID
			node.accountHi = accountHi
			node.accountLo = accountLo
			self.entity_def = node
			self.current_node.append(node)
			self.game.playernodes[id] = node
			return

		if data == "CREATE_GAME":
			self.create_game(ts)
			return

		if data == "ACTION_END":
			if not hasattr(self.current_node, "parent"):
				# Urgh, this happens all the time with mulligans :(
				# sys.stderr.write("Warning: Node %r has no parent\n" % (self.current_node))
				return
			self.current_node = self.current_node.parent
			return

		sys.stderr.write("Warning: Unhandled data: %r\n" % (data))

	def create_game(self, ts):
		self.game = GameNode(ts)
		self.game.players = {}
		self.game.playernodes = {}
		self.current_node = self.game
		self.current_node.indent_level = 0
		self.ast.append(self.game)

	def handle_options(self, ts, data):
		data = data.lstrip()

		sre = OPTIONS_ENTITY_RE.match(data)
		if sre:
			id, = sre.groups()
			node = OptionsNode(ts, id)
			self.current_options_node = node
			self.current_node.append(node)
			return

		sre = OPTIONS_OPTION_RE.match(data)
		if sre:
			index, type, entity = sre.groups()
			entity = self._parse_entity(entity)
			node = OptionNode(index, type, entity)
			self.current_options_node.append(node)
			self.current_option_node = node
			# last_option_node lets us differenciate between
			# target for option and target for suboption
			self.last_option_node = node
			return

		sre = OPTIONS_SUBOPTION_RE.match(data)
		if sre:
			subop_type, index, entity = sre.groups()
			entity = self._parse_entity(entity)
			if subop_type == "subOption":
				node = SubOptionNode(index, entity)
				self.current_option_node.append(node)
				self.last_option_node = node
			else:  # subop_type == "target"
				node = OptionTargetNode(index, entity)
				self.last_option_node.append(node)
			return

		sys.stderr.write("Warning: Unimplemented options: %r\n" % (data))

	def handle_send_option(self, ts, data):
		data = data.lstrip()

		sre = SEND_OPTION_RE.match(data)
		if sre:
			option, suboption, target, position = sre.groups()
			node = SendOptionNode(ts, option, suboption, target, position)
			self.current_node.append(node)

	def toxml(self):
		root = ElementTree.Element("HearthstoneReplay")
		for game in self.ast:
			root.append(game.xml())
		return pretty_xml(root)


def main():
	fname = sys.argv[1]
	parser = PowerLogParser()

	with open(fname, "r") as f:
		parser.read(f)

	print(parser.toxml())


if __name__ == "__main__":
	main()
