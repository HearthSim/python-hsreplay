from dateutil.parser import parse as parse_timestamp
from hearthstone.hslog import packets
from .utils import ElementTree


def node_for_tagname(tag):
	for k, v in globals().items():
		if k.endswith("Node") and v.tagname == tag:
			return v
	raise ValueError("No matching node for tag %r" % (tag))


class Node(object):
	attributes = ()
	tagname = None

	def __init__(self, *args):
		self._attributes = {}
		self.nodes = []
		for k, arg in zip(("ts", ) + self.attributes, args):
			setattr(self, k, arg)

	def __repr__(self):
		return "<%s>" % (self.__class__.__name__)

	@classmethod
	def from_xml(cls, xml):
		if xml.tag != cls.tagname:
			raise ValueError("%s.from_xml() called with %r, not %r" % (
				cls.__name__, xml.tag, cls.tagname
			))
		ts = xml.attrib.get("ts")
		if ts:
			ts = parse_timestamp(ts)
		ret = cls(ts)
		for element in xml:
			ecls = node_for_tagname(element.tag)
			node = ecls.from_xml(element)
			for attrname in ecls.attributes:
				setattr(node, attrname, element.attrib.get(attrname))
			ret.nodes.append(node)
		return ret

	def append(self, node):
		self.nodes.append(node)

	def xml(self):
		element = ElementTree.Element(self.tagname)
		for node in self.nodes:
			element.append(node.xml())
		for attr in self.attributes:
			attrib = getattr(self, attr, None)
			if attrib is not None:
				if isinstance(attrib, bool):
					attrib = str(attrib).lower()
				elif isinstance(attrib, int):
					# Check for enums
					attrib = str(int(attrib))
				element.attrib[attr] = attrib
		if self.timestamp and self.ts:
			element.attrib["ts"] = self.ts.isoformat()

		for k, v in self._attributes.items():
			element.attrib[k] = v

		return element


class GameNode(Node):
	tagname = "Game"
	attributes = ("id", "reconnecting")
	timestamp = True
	packet_class = packets.PacketTree

	@property
	def players(self):
		return self.nodes[1:3]

	def export(self):
		tree = self.packet_class(self.ts)
		create_game = self.nodes[0].export()

		for player in self.players:
			create_game.players.append(player.export())
		tree.packets.append(create_game)

		for node in self.nodes[3:]:
			tree.packets.append(node.export())
		return tree


class GameEntityNode(Node):
	tagname = "GameEntity"
	attributes = ("id", )
	timestamp = False
	packet_class = packets.CreateGame

	def export(self):
		packet = self.packet_class(self.ts, int(self.id))
		for node in self.nodes:
			packet.tags.append(node.export())
		return packet


class PlayerNode(Node):
	tagname = "Player"
	attributes = (
		"id", "playerID", "accountHi", "accountLo", "name",
		"rank", "legendRank", "cardback"
	)
	timestamp = False
	packet_class = packets.CreateGame.Player

	def export(self):
		packet = self.packet_class(
			self.ts, int(self.id), int(self.playerID),
			int(self.accountHi), int(self.accountLo)
		)
		packet.name = self.name
		for node in self.nodes:
			if node.tagname == "Tag":
				packet.tags.append(node.export())
		return packet

	def xml(self):
		ret = super(PlayerNode, self).xml()
		deck = getattr(self, "deck", None)
		if deck is not None:
			element = ElementTree.Element("Deck")
			ret.append(element)
			for card in deck:
				e = ElementTree.Element("Card")
				e.attrib["id"] = card
				element.append(e)

		return ret


class DeckNode(Node):
	tagname = "Deck"
	attributes = ()
	timestamp = False
	packet_class = None


class CardNode(Node):
	tagname = "Card"
	attributes = ("id", "premium")
	timestamp = False
	packet_class = None


class FullEntityNode(Node):
	tagname = "FullEntity"
	attributes = ("id", "cardID")
	timestamp = False
	packet_class = packets.FullEntity

	def export(self):
		packet = self.packet_class(self.ts, int(self.id), self.cardID)
		for node in self.nodes:
			packet.tags.append(node.export())
		return packet


class ShowEntityNode(Node):
	tagname = "ShowEntity"
	attributes = ("entity", "cardID")
	timestamp = False
	packet_class = packets.ShowEntity

	def export(self):
		packet = self.packet_class(self.ts, int(self.entity), self.cardID)
		for node in self.nodes:
			packet.tags.append(node.export())
		return packet


class BlockNode(Node):
	tagname = "Block"
	attributes = ("entity", "type", "index", "target")
	timestamp = True
	packet_class = packets.Block

	def export(self):
		index = int(self.index) if self.index is not None else -1
		packet = self.packet_class(
			self.ts, int(self.entity or 0), int(self.type), index,
			None, None, int(self.target or 0)
		)
		for node in self.nodes:
			packet.packets.append(node.export())
		packet.ended = True
		return packet


class MetaDataNode(Node):
	tagname = "MetaData"
	attributes = ("meta", "data", "info")
	timestamp = False
	packet_class = packets.MetaData

	def export(self):
		packet = self.packet_class(
			self.ts, int(self.meta), int(self.data or 0), int(self.info)
		)
		for node in self.nodes:
			packet.info.append(node.export())
		return packet


class MetaDataInfoNode(Node):
	tagname = "Info"
	attributes = ("index", "entity")
	timestamp = False

	def export(self):
		return int(self.entity)


class TagNode(Node):
	tagname = "Tag"
	attributes = ("tag", "value")
	timestamp = False

	def export(self):
		return (int(self.tag), int(self.value))


class TagChangeNode(Node):
	tagname = "TagChange"
	attributes = ("entity", "tag", "value")
	timestamp = False
	packet_class = packets.TagChange

	def export(self):
		return self.packet_class(self.ts, int(self.entity), int(self.tag), int(self.value))


class HideEntityNode(Node):
	tagname = "HideEntity"
	attributes = ("entity", "zone")
	timestamp = True
	packet_class = packets.HideEntity

	def export(self):
		return self.packet_class(self.ts, int(self.entity), int(self.zone))


class ChangeEntityNode(Node):
	tagname = "ChangeEntity"
	attributes = ("entity", "cardID")
	timestamp = True
	packet_class = packets.ChangeEntity

	def export(self):
		packet = self.packet_class(self.ts, int(self.entity), self.cardID)
		for node in self.nodes:
			packet.tags.append(node.export())
		return packet


##
# Choices

class ChoicesNode(Node):
	tagname = "Choices"
	attributes = ("entity", "id", "taskList", "type", "min", "max", "source")
	timestamp = True
	packet_class = packets.Choices

	def export(self):
		taskList = int(self.taskList) if self.taskList else None
		packet = self.packet_class(
			self.ts, int(self.entity or 0), int(self.id), taskList,
			int(self.type), int(self.min), int(self.max)
		)
		packet.source = self.source
		for node in self.nodes:
			packet.choices.append(node.export())
		return packet


class ChoiceNode(Node):
	tagname = "Choice"
	attributes = ("index", "entity")
	timestamp = False

	def export(self):
		return int(self.entity)


class ChosenEntitiesNode(Node):
	tagname = "ChosenEntities"
	attributes = ("entity", "id")
	timestamp = True
	packet_class = packets.ChosenEntities

	def export(self):
		packet = self.packet_class(self.ts, int(self.entity), int(self.id))
		for node in self.nodes:
			packet.choices.append(node.export())
		return packet


class SendChoicesNode(Node):
	tagname = "SendChoices"
	attributes = ("id", "type")
	timestamp = True
	packet_class = packets.SendChoices

	def export(self):
		packet = self.packet_class(self.ts, int(self.id), int(self.type))
		for node in self.nodes:
			packet.choices.append(node.export())
		return packet


##
# Options

class OptionsNode(Node):
	tagname = "Options"
	attributes = ("id", )
	timestamp = True
	packet_class = packets.Options

	def export(self):
		packet = self.packet_class(self.ts, int(self.id))
		for i, node in enumerate(self.nodes):
			packet.options.append(node.export(i))
		return packet


class OptionNode(Node):
	tagname = "Option"
	attributes = ("index", "entity", "type")
	timestamp = False
	packet_class = packets.Option

	def export(self, id):
		optype = "option"
		packet = self.packet_class(self.ts, int(self.entity or 0), id, int(self.type), optype)
		for i, node in enumerate(self.nodes):
			packet.options.append(node.export(i))
		return packet


class SubOptionNode(Node):
	tagname = "SubOption"
	attributes = ("index", "entity")
	timestamp = False
	packet_class = packets.Option

	def export(self, id):
		optype = "subOption"
		type = None
		packet = self.packet_class(self.ts, int(self.entity), id, type, optype)
		for i, node in enumerate(self.nodes):
			packet.options.append(node.export(i))
		return packet


class OptionTargetNode(Node):
	tagname = "Target"
	attributes = ("index", "entity")
	timestamp = False
	packet_class = packets.Option

	def export(self, id):
		optype = "target"
		type = None
		return self.packet_class(self.ts, int(self.entity), id, type, optype)


class SendOptionNode(Node):
	tagname = "SendOption"
	attributes = ("option", "subOption", "target", "position")
	timestamp = True
	packet_class = packets.SendOption

	def export(self):
		return self.packet_class(
			self.ts, int(self.option), int(self.subOption), int(self.target), int(self.position)
		)
