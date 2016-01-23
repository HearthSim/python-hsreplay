#!/usr/bin/env python
import re
import sys, os, zipfile
import json
from zipfile import ZipFile
from hearthstone import enums
from hearthstone.enums import GameTag
from xml.etree import ElementTree
from xml.dom import minidom


__version__ = "1.0"

SYSTEM_DTD = "http://hearthsim.info/hsreplay/dtd/hsreplay-%s.dtd" % (__version__)

_E = r"(GameEntity|UNKNOWN HUMAN PLAYER|\[.+\]|\d+|.+)"

POWERLOG_LINE_RE = re.compile(r"^D ([\d:.]+) ([^(]+)\(\) - (.+)$")
OUTPUTLOG_LINE_RE = re.compile(r"\[Power\] ()([^(]+)\(\) - (.+)$")

ENTITY_RE = re.compile("\[.*\s*id=(\d+)\s*.*\]")

CHOICES_CHOICE_RE_OLD = re.compile(r"id=(\d+) PlayerId=(\d+) ChoiceType=(\w+) CountMin=(\d+) CountMax=(\d+)$")
CHOICES_CHOICE_RE = re.compile(r"id=(\d+) Player=%s TaskList=(\d+)? ChoiceType=(\w+) CountMin=(\d+) CountMax=(\d+)$" % _E)
CHOICES_SOURCE_RE = re.compile(r"Source=%s$" % _E)
CHOICES_ENTITIES_RE = re.compile(r"Entities\[(\d+)\]=(\[.+\])$")

ENTITIES_CHOSEN_RE = re.compile(r"id=(\d+) Player=%s EntitiesCount=(\d+)$" % _E)
ENTITIES_CHOSEN_ENTITIES_RE = re.compile(r"Entities\[(\d+)\]=%s$" % _E)

SEND_CHOICES_CHOICETYPE_RE = re.compile(r"id=(\d+) ChoiceType=(.+)$")
SEND_CHOICES_ENTITIES_RE = re.compile(r"m_chosenEntities\[(\d+)\]=(\[.+\])$")

OPTIONS_ENTITY_RE = re.compile(r"id=(\d+)$")
OPTIONS_OPTION_RE = re.compile(r"option (\d+) type=(\w+) mainEntity=%s?$" % _E)
OPTIONS_SUBOPTION_RE = re.compile(r"(subOption|target) (\d+) entity=%s?$" % _E)

SEND_OPTION_RE = re.compile(r"selectedOption=(\d+) selectedSubOption=(-1|\d+) selectedTarget=(\d+) selectedPosition=(\d+)")

ACTION_TAG_RE = re.compile(r"tag=(\w+) value=(\w+)")
ACTION_FULLENTITY_CREATE_RE = re.compile(r"FULL_ENTITY - Creating ID=(\d+) CardID=(\w+)?$")
ACTION_FULLENTITY_UPDATE_RE = re.compile(r"FULL_ENTITY - Updating %s CardID=(\w+)?$" % _E)
ACTION_SHOWENTITY_RE = re.compile(r"SHOW_ENTITY - Updating Entity=%s CardID=(\w+)$" % _E)
ACTION_HIDEENTITY_RE = re.compile(r"HIDE_ENTITY - Entity=%s tag=(\w+) value=(\w+)$" % _E)
ACTION_TAGCHANGE_RE = re.compile(r"TAG_CHANGE Entity=%s tag=(\w+) value=(\w+)" % _E)
ACTION_START_RE = re.compile(r"ACTION_START Entity=%s (?:SubType|BlockType)=(\w+) Index=(-1|\d+) Target=%s$" % (_E, _E))
ACTION_METADATA_RE = re.compile(r"META_DATA - Meta=(\w+) Data=%s Info=(\d+)" % _E)
ACTION_METADATA_INFO_RE = re.compile(r"Info\[(\d+)\] = %s" % _E)
ACTION_CREATEGAME_RE = re.compile(r"GameEntity EntityID=(\d+)")
ACTION_CREATEGAME_PLAYER_RE = re.compile(r"Player EntityID=(\d+) PlayerID=(\d+) GameAccountId=\[hi=(\d+) lo=(\d+)\]$")


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
			if attrib:
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

	def register_player_id(self, entity, id):
		# Power.log sucks, the entity IDs for players are not reliable.
		# We convert them to actual entity IDs...
		if entity == "UNKNOWN HUMAN PLAYER":
			# Never register unknown players, for our own sanity
			return
		if entity in self.players:
			# Just making sure we're not corrupting data...
			if self.players[entity] != id:
				sys.stderr.write("Warning: cannot match player %r to entity ID\n" % (entity))
				return
		self.players[entity] = id
		self.playernodes[id].name = entity

	def update_current_player(self, entity, value):
		# 2nd method of figuring out the player ids: through the CURRENT_PLAYER tag
		if len(self.players) == 2:
			# Skip it if we already have both players
			return
		if value == "0" and self.first_player:
			self.register_player_id(entity, self.first_player)
			self.second_player = [p for p in self.playernodes if p != self.first_player][0]
		elif value == "1" and self.second_player:
			self.register_player_id(entity, self.second_player)
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
	attributes = ("meta", "data", "info")
	timestamp = False


class MetaDataInfoNode(Node):
	tagname = "Info"
	attributes = ("index", "id")
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
	attributes = ("entity", "playerID", "taskList", "type", "min", "max", "source")
	timestamp = True


class ChoiceNode(Node):
	tagname = "Choice"
	attributes = ("index", "entity")
	timestamp = False


class ChosenEntitiesNode(Node):
	tagname = "ChosenEntities"
	attributes = ("entity", "playerID", "count")
	timestamp = True


class SendChoicesNode(Node):
	tagname = "SendChoices"
	attributes = ("entity", "type")
	timestamp = True


##
# Options

class OptionsNode(Node):
	tagname = "Options"
	attributes = ("id", )
	timestamp = True


class OptionNode(Node):
	tagname = "Option"
	attributes = ("index", "type", "entity")
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


class PlayerID:
	def __init__(self, game, data):
		self.game = game
		self.data = data

	def __contains__(self, other):
		return str(self).__contains__(other)

	def __str__(self):
		if self.data not in self.game.players:
			sys.stderr.write("Warning: Could not match %r to an entity id.\n" % (self.data))
		return self.game.players.get(self.data, self.data)


TAG_TYPES = {
	GameTag.CARDTYPE: enums.CardType,
	GameTag.CLASS: enums.CardClass,
	GameTag.FACTION: enums.Faction,
	GameTag.PLAYSTATE: enums.PlayState,
	GameTag.RARITY: enums.Rarity,
	GameTag.MULLIGAN_STATE: enums.Mulligan,
	GameTag.NEXT_STEP: enums.Step,
	GameTag.STATE: enums.State,
	GameTag.STEP: enums.Step,
	GameTag.ZONE: enums.Zone,
}


def parse_enum(enum, value):
	if value.isdigit():
		value = int(value)
	elif hasattr(enum, value):
		value = getattr(enum, value)
	else:
		sys.stderr.write("Warning: Unhandled %s: %r\n" % (enum, value))
	return value


def parse_tag(tag, value):
	tag = parse_enum(GameTag, tag)
	if tag in TAG_TYPES:
		value = parse_enum(TAG_TYPES[tag], value)
	elif value.isdigit():
		value = int(value)
	else:
		sys.stderr.write("Unhandled string value: %r = %r" % (tag, value))
	return tag, value


class PowerLogParser:
	def __init__(self):
		self.ast = []
		self.current_node = None
		self.metadata_node = None

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

		if data == "UNKNOWN HUMAN PLAYER":
			return "[UNKNOWN HUMAN PLAYER]"

		if data.isdigit():
			return data

		return PlayerID(self.game, data)

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

	def update_node(self, node):
		if self.current_node is None:
			# Incomplete game
			sys.stderr.write("Warning: Creating an incomplete game\n")
			self.create_game(ts="")
		self.current_node.append(node)

	def add_data(self, ts, method, data):
		# if method == "PowerTaskList.DebugPrintPower":
		if method == "GameState.DebugPrintPower":
			self.handle_data(ts, data)
		elif method == "GameState.SendChoices":
			self.handle_send_choices(ts, data)
		elif method == "GameState.DebugPrintChoices":
			self.handle_choices(ts, data)
		elif method == "GameState.DebugPrintEntityChoices":
			self.handle_choices(ts, data)
		elif method == "GameState.DebugPrintEntitiesChosen":
			self.handle_entities_chosen(ts, data)
		elif method == "GameState.DebugPrintOptions":
			self.handle_options(ts, data)
		elif method == "GameState.SendOption":
			self.handle_send_option(ts, data)
		elif method == "GameState.DebugPrintChoice":
			sys.stderr.write("Warning: DebugPrintChoice was removed in 10357. Ignoring.\n")
		elif method == "ChoiceCardMgr.WaitThenShowChoices":
			# Not needed for replays
			pass
		elif method == "GameState.DebugPrintPowerList":
			# We don't need this
			pass
		elif method == "GameState.OnEntityChoices":
			# Spectator mode noise
			pass
		else:
			if not method.startswith(("PowerTaskList.", "PowerProcessor.", "PowerSpellController")):
				sys.stderr.write("Warning: Unhandled method %r\n" % (method))

	def handle_send_choices(self, ts, data):
		data = data.lstrip()

		sre = SEND_CHOICES_CHOICETYPE_RE.match(data)
		if sre:
			id, type = sre.groups()
			type = parse_enum(enums.ChoiceType, type)
			node = SendChoicesNode(ts, id, type)
			self.update_node(node)
			self.current_send_choice_node = node
			return

		sre = SEND_CHOICES_ENTITIES_RE.match(data)
		if sre:
			index, entity = sre.groups()
			entity = self._parse_entity(entity)
			node = ChoiceNode(ts, index, entity)
			self.current_send_choice_node.append(node)
			return

		sys.stderr.write("Warning: Unhandled sent choices: %r\n" % (data))

	def handle_entities_chosen(self, ts, data):
		# New in 10357
		data = data.lstrip()

		sre = ENTITIES_CHOSEN_RE.match(data)
		if sre:
			entity, player, count = sre.groups()
			entity = self._parse_entity(entity)
			# NOTE: in 10357, "Player" is bugged, it's treating a player ID
			# as an entity ID, resulting in "Player=GameEntity"
			# For our own sanity we keep the old playerID logic from the
			# previous builds, we'll change to "player" when it's fixed.
			playerID = self._parse_entity(player)
			# assert str(playerID).isdigit()
			node = ChosenEntitiesNode(ts, entity, playerID, count)
			self.game.append(node)
			self.current_chosen_entities_node = node
			return

		sre = ENTITIES_CHOSEN_ENTITIES_RE.match(data)
		if sre:
			index, entity = sre.groups()
			entity = self._parse_entity(entity)
			node = ChoiceNode(ts, index, entity)
			self.current_chosen_entities_node.append(node)
			return

		sys.stderr.write("Warning: Unhandled chosen entities: %r\n" % (data))

	def handle_choices(self, ts, data):
		data = data.lstrip()

		# pre-10357 choices
		sre = CHOICES_CHOICE_RE_OLD.match(data)
		if sre:
			entity, playerID, type, min, max = sre.groups()
			type = parse_enum(enums.ChoiceType, type)
			taskList = None
			node = ChoicesNode(ts, entity, playerID, taskList, type, min, max, None)
			self.current_node.append(node)
			self.current_choice_node = node
			return

		sre = CHOICES_CHOICE_RE.match(data)
		if sre:
			entity, player, taskList, type, min, max = sre.groups()
			# tasklist can be empty eg. in spectator mode
			# NOTE: in 10357, "Player" is bugged, it's treating a player ID
			# as an entity ID, resulting in "Player=GameEntity"
			# For our own sanity we keep the old playerID logic from the
			# previous builds, we'll change to "player" when it's fixed.
			player = self._parse_entity(player)
			# assert str(player).isdigit()
			type = parse_enum(enums.ChoiceType, type)
			node = ChoicesNode(ts, entity, player, taskList, type, min, max, None)
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
			node = ChoiceNode(ts, index, entity)
			self.current_choice_node.append(node)
			return

		sys.stderr.write("Warning: Unhandled choices: %r\n" % (data))

	def handle_data(self, ts, data):
		# print(data)
		stripped_data = data.lstrip()
		indent_level = len(data) - len(stripped_data)
		data = stripped_data

		sre = ACTION_TAG_RE.match(data)
		if sre:
			tag, value = sre.groups()
			tag, value = parse_tag(tag, value)
			if tag == GameTag.CURRENT_PLAYER:
				assert isinstance(self.entity_def, PlayerNode)
				self.game.first_player = self.entity_def.id
			node = TagNode(ts, tag, value)
			assert self.entity_def
			self.entity_def.append(node)
			return

		sre = ACTION_TAGCHANGE_RE.match(data)
		if sre:
			self.entity_def = None
			entity, tag, value = sre.groups()
			tag, value = parse_tag(tag, value)
			if tag == GameTag.ENTITY_ID:
				if not entity.isdigit() and not entity.startswith("[") and entity != "GameEntity":
					self.game.register_player_id(entity, str(value))
			elif tag == GameTag.CURRENT_PLAYER:
				self.game.update_current_player(entity, str(value))
			entity = self._parse_entity(entity)
			node = TagChangeNode(ts, entity, tag, value)

			self.update_node(node)
			self.current_node.indent_level = indent_level
			return

		sre = ACTION_FULLENTITY_CREATE_RE.match(data)
		if not sre:
			# Updating an existing entity through a FullEntity tag is rare but
			# it is possible and not illegal.
			sre = ACTION_FULLENTITY_UPDATE_RE.match(data)
		if sre:
			entity, cardid = sre.groups()
			entity = self._parse_entity(entity)
			node = FullEntityNode(ts, entity, cardid)
			self.entity_def = node
			self.update_node(node)
			return

		sre = ACTION_SHOWENTITY_RE.match(data)
		if sre:
			entity, cardid = sre.groups()
			entity = self._parse_entity(entity)
			node = ShowEntityNode(ts, entity, cardid)
			self.entity_def = node
			self.update_node(node)
			return

		sre = ACTION_HIDEENTITY_RE.match(data)
		if sre:
			entity, tag, value = sre.groups()
			entity = self._parse_entity(entity)
			tag, zone = parse_tag(tag, value)
			assert tag == GameTag.ZONE
			node = HideEntityNode(ts, entity, zone)
			self.update_node(node)
			return

		sre = ACTION_START_RE.match(data)
		if sre:
			entity, type, index, target = sre.groups()
			entity = self._parse_entity(entity)
			type = parse_enum(enums.PowSubType, type)
			target = self._parse_entity(target)
			node = ActionNode(ts, entity, type, index, target)
			self.update_node(node)
			node.parent = self.current_node
			self.current_node = node
			self.current_node.indent_level = indent_level
			return

		sre = ACTION_METADATA_RE.match(data)
		if sre:
			meta, data, info = sre.groups()
			meta = parse_enum(enums.MetaDataType, meta)
			data = self._parse_entity(data)
			node = MetaDataNode(ts, meta, data, info)
			if not isinstance(self.current_node, ActionNode):
				sys.stderr.write(
					"Warning: META_DATA node present outside an Action block\n"
					"This is not officially supported. "
					"See https://github.com/HearthSim/hs-bugs/issues/260\n"
				)
			self.update_node(node)
			self.metadata_node = node
			return

		sre = ACTION_METADATA_INFO_RE.match(data)
		if sre:
			index, entity = sre.groups()
			entity = self._parse_entity(entity)
			node = MetaDataInfoNode(ts, index, entity)
			self.metadata_node.append(node)
			return

		sre = ACTION_CREATEGAME_RE.match(data)
		if sre:
			id, = sre.groups()
			assert id == "1"
			self.game.id = id
			node = GameEntityNode(ts, id)
			self.update_node(node)
			self.entity_def = node
			return

		sre = ACTION_CREATEGAME_PLAYER_RE.match(data)
		if sre:
			id, playerID, accountHi, accountLo = sre.groups()
			node = PlayerNode(ts, id, playerID, accountHi, accountLo, None)
			self.entity_def = node
			self.update_node(node)
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
			self.update_node(node)
			return

		sre = OPTIONS_OPTION_RE.match(data)
		if sre:
			index, type, entity = sre.groups()
			type = parse_enum(enums.OptionType, type)
			entity = self._parse_entity(entity)
			node = OptionNode(ts, index, type, entity)
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
				node = SubOptionNode(ts, index, entity)
				self.current_option_node.append(node)
				self.last_option_node = node
			else:  # subop_type == "target"
				node = OptionTargetNode(ts, index, entity)
				self.last_option_node.append(node)
			return

		sys.stderr.write("Warning: Unimplemented options: %r\n" % (data))

	def handle_send_option(self, ts, data):
		data = data.lstrip()

		sre = SEND_OPTION_RE.match(data)
		if sre:
			option, suboption, target, position = sre.groups()
			node = SendOptionNode(ts, option, suboption, target, position)
			self.update_node(node)

	def toxml(self):
		builder = ElementTree.TreeBuilder()
		builder.start("HSReplay", {"version": __version__})
		builder.end("HSReplay")
		root = builder.close()
		for game in self.ast:
			root.append(game.xml())
		return pretty_xml(root)
def main():
	array = []
	if len(sys.argv) == 1:
		print( "Usage")
		print( "main.py [file] : will convert a log file in a .hsreplay file")
		print( "main.py -all [folder] : will convert all .hdtreplay files in .hsreplay files")
		print( "main.py -help display help")
	if len(sys.argv) > 1:
		if sys.argv[1] == "-help":
			print( "Usage")
			print( "main.py [file] : will convert a log file in a .hsreplay file")
			print( "main.py -all [folder] : will convert all .hdtreplay files in .hsreplay files")
			print( "main.py -help display help")
		# I had this -all option 
		if sys.argv[1] == "-all":
			dirs = os.listdir( sys.argv[2] )
			i = 0
			j = 0
			for item in dirs:
				try:
					if i == 100:
						break
					# unzip the output_log.txt file
					with ZipFile(sys.argv[2]+item, 'r') as myzip:
						myzip.extractall(sys.argv[2])
					fname = sys.argv[2]+"output_log.txt"
					parser = PowerLogParser()
					with open(fname, "w") as f:
						f.write("[Power] GameState.DebugPrintPower() - CREATE_GAME")
					with open(fname, "r") as f:
						parser.read(f)
					name = item.replace(' ','')
					print(name)
					finalfilename = sys.argv[2]+item[0:len(item)-len(".hdtreplay")]+'.hsreplay'
					with open(finalfilename, "w") as f:
						f.write(parser.toxml())
					i = i+1
					j = j+1
					rate = (j/i) * 100
					print(item+" convertion success"+str(rate))
				except:
					i = i+1
					array.append(fname)
					print('An exception occurred')
			with open('errors.txt', 'w') as outfile:
				json.dump(array, outfile)

		else:
			fname = sys.argv[1]
			parser = PowerLogParser()
			
			with open(fname, "r") as f:
				parser.read(f)

			print(parser.toxml())
if __name__ == "__main__":
	main()
