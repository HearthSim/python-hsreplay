#!/usr/bin/env python
import sys
from xml.etree import ElementTree


def indented(packets, level=1):
	ret = [str(p) for p in packets]
	indent = "\t" * level
	ret = indent + "\n".join(ret)
	return ("\n" + indent).join(ret.split("\n"))


def get_packet_class(element):
	return globals().get(element.tag, Packet)


class Packet:
	def __init__(self, game, element):
		self.packets = [get_packet_class(e)(game, e) for e in element]
		self.name = element.tag
		self.game = game

		for k, v in element.attrib.items():
			setattr(self, k, v)

	def __repr__(self):
		return "<%s>" % (self.name)

	def format_entity(self, entity):
		if entity == 1:
			return "GameEntity"
		if entity in self.game.state:
			e = self.game.state[entity]
			cardID = getattr(e, "cardID", None)
			if cardID:
				return "[name=%s id=%i cardId=%s]" % ("", e.id, cardID)
		return str(entity)


class _EntityPacket(Packet):
	def __init__(self, *args):
		super().__init__(*args)
		self.id = int(self.id)
		self.game.state[self.id] = self


class Game(Packet):
	def __init__(self, element):
		self.state = {}
		super().__init__(self, element)

	def __str__(self):
		return "CREATE_GAME\n" + indented(self.packets)


class GameEntity(_EntityPacket):
	def __str__(self):
		ret = "GameEntity EntityID=%i\n" % self.args()
		return ret + indented(self.packets)

	def args(self):
		return self.id


class Player(_EntityPacket):
	def __str__(self):
		ret = "Player EntityID=%i PlayerID=%i GameAccountId=[hi=%i lo=%i]" % self.args()
		# Adding the name to our own logs because Blizzard's format sucks
		ret += " Name=%s\n" % (self.name)
		return ret + indented(self.packets)

	def args(self):
		return self.id, int(self.playerID), int(self.accountHi), int(self.accountLo)


class Action(Packet):
	def __str__(self):
		start = "ACTION_START Entity=%s BlockType=%s Index=%i Target=%s\n" % self.args()
		return start + "%s\nACTION_END" % (indented(self.packets))

	def args(self):
		return self.entity, self.type, int(self.index), getattr(self, "target", 0)


class FullEntity(_EntityPacket):
	def __str__(self):
		ret = "FULL_ENTITY - Creating ID=%i CardID=%s\n" % self.args()
		return ret + indented(self.packets)

	def args(self):
		return self.id, getattr(self, "cardID", "")


class Tag(Packet):
	def __str__(self):
		return "tag=%s value=%s" % self.args()

	def args(self):
		return self.tag, self.value


class ShowEntity(Packet):
	def __str__(self):
		ret = "SHOW_ENTITY - Updating Entity=%s CardID=%s\n" % self.args()
		return ret + indented(self.packets)

	def args(self):
		return self.format_entity(self.entity), self.cardID


class HideEntity(Packet):
	def __str__(self):
		return "HIDE_ENTITY - Entity=%s tag=%s value=%s" % self.args()

	def args(self):
		return self.format_entity(self.entity), self.tag, self.value


class TagChange(Packet):
	def __str__(self):
		return "TAG_CHANGE Entity=%s tag=%s value=%s" % self.args()

	def args(self):
		return self.format_entity(int(self.entity)), self.tag, self.value


class Choices(Packet):
	def __str__(self):
		ret = "CHOICES - id=%i PlayerId=%i ChoiceType=%s CountMin=%i CountMax=%i\n" % self.args()
		return ret + "\tSource=%s\n" % (self.entity) + indented(self.packets)

	def args(self):
		return int(self.entity), int(self.playerID), self.type, int(self.min), int(self.max)


class Options(Packet):
	def __str__(self):
		ret = "OPTIONS - id=%i\n" % self.args()
		return ret + indented(self.packets)

	def args(self):
		return int(self.id)


class Option(Packet):
	def __str__(self):
		return "option %i type=%s mainEntity=%s" % self.args()

	def args(self):
		return int(self.index), self.type, getattr(self, "entity", "")


class SendOption(Packet):
	def __str__(self):
		return "SEND_OPTION - selectedOption=%i selectedSubOption=%i selectedTarget=%i selectedPosition=%i" % self.args()

	def args(self):
		return int(self.option), int(self.subOption), int(self.target), int(self.position)


class Choice(Packet):
	def __str__(self):
		return "Entities[%i]=%s" % self.args()

	def args(self):
		return int(self.index), self.entity


class SendChoices(Packet):
	def __str__(self):
		ret = "SEND_CHOICES - id=%i ChoiceType=%s\n" % self.args()
		return ret + indented(self.packets)

	def args(self):
		return int(self.entity), self.type


class MetaData(Packet):
	def __str__(self):
		ret = "META_DATA - Meta=%s Data=%i Info=%i\n" % self.args()
		return ret + indented(self.packets)

	def args(self):
		return self.meta, int(getattr(self, "data", 0)), int(self.info)


class Info(Packet):
	def __str__(self):
		return "Info[%i] = %s" % self.args()

	def args(self):
		return int(self.index), self.id


class XMLParser:
	def __init__(self):
		self.games = []

	def load(self, f):
		xml = ElementTree.parse(f)
		for game in xml.findall("Game"):
			self.game = Game(game)
			self.games.append(self.game)


def main():
	parser = XMLParser()
	for fname in sys.argv[1:]:
		with open(fname, "r") as f:
			parser.load(f)
			for game in parser.games:
				print(game)


if __name__ == "__main__":
	main()
