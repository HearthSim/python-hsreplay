#!/usr/bin/env python
import re
import sys


POWERLOG_LINE_RE = re.compile(r"^D ([\d:.]+) ([^(]+)\(\) - (.+)$")

ENTITY_RE = re.compile("\[.*\s*id=(\d+)\s*.*\]")

CHOICES_CHOICETYPE_RE = re.compile(r"^id=(\d+) ChoiceType=(.+)$")
CHOICES_ENTITIES_RE = re.compile(r"m_chosenEntities\[(\d+)\]=(\[.+\])$")

OPTIONS_ENTITY_RE = re.compile(r"id=(\d+)$")
OPTIONS_OPTION_RE = re.compile(r"option (\d+) type=(\w+) mainEntity=(.*)$")
OPTIONS_SUBOPTION_RE = re.compile(r"(subOption|target) (\d+) entity=(.*)$")

ACTION_SHOWENTITY_TAG_RE = re.compile(r"tag=(\w+) value=(\w+)")
ACTION_FULLENTITY_RE_1 = re.compile(r"FULL_ENTITY - Updating (\[.+\]) CardID=(\w+)?$")
ACTION_FULLENTITY_RE_2 = re.compile(r"FULL_ENTITY - Creating ID=(\d+) CardID=(\w+)?$")
ACTION_SHOWENTITY_RE = re.compile(r"SHOW_ENTITY - Updating Entity=(\[?.+\]?) CardID=(\w+)$")
ACTION_HIDEENTITY_RE = re.compile(r"HIDE_ENTITY - Entity=(\[.+\]) tag=(\w+) value=(\w+)")
ACTION_TAGCHANGE_RE = re.compile(r"TAG_CHANGE Entity=(\[?.+\]?) tag=(\w+) value=(\w+)")
ACTION_START_RE = re.compile(r"ACTION_START Entity=(\[?.+\]?) BlockType=(\w+) Index=(-1|\d+) Target=(\[?.+\]?)$")
ACTION_METADATA_RE = re.compile(r"META_DATA - Meta=(\w+) Data=(\d+) Info=(\d+)")
ACTION_CREATEGAME_RE = re.compile(r"GameEntity EntityID=(\d+)")
ACTION_CREATEGAME_PLAYER_RE = re.compile(r"Player EntityID=(\d+) PlayerID=(\d+) GameAccountId=\[hi=(\d+) lo=(\d+)\]$")


class PowerLogParser:
	def __init__(self):
		self.ast = []

	def _parse_entity(self, data):
		if not data:
			return None
		sre = ENTITY_RE.match(data)
		if sre:
			id = int(sre.groups()[0])
			return id

		if data == "0":
			return None

		if data == "GameEntity":
			return "GameEntity"

		# TODO handle <AccountName>
		return data

	def read(self, f):
		for line in f.readlines():
			sre = POWERLOG_LINE_RE.match(line)
			if not sre:
				continue

			self.add_data(*sre.groups())

	def add_data(self, timestamp, method, data):
		# if method == "PowerTaskList.DebugPrintPower":
		if method == "GameState.DebugPrintPower":
			self.handle_data(timestamp, data)
		elif method == "GameState.SendChoices":
			self.handle_choices(timestamp, data)
		elif method == "GameState.DebugPrintOptions":
			self.handle_options(timestamp, data)

	def handle_choices(self, timestamp, data):
		sre = CHOICES_CHOICETYPE_RE.match(data)
		if sre:
			entityid, choicetype = sre.groups()
			return

		sre = CHOICES_ENTITIES_RE.match(data)
		if sre:
			choiceid, entity = sre.groups()
			entity = self._parse_entity(entity)
			return

	def handle_data(self, timestamp, data):
		data = data.lstrip()
		sre = ACTION_SHOWENTITY_TAG_RE.match(data)
		if sre:
			tag, value = sre.groups()
			# print("Setting %r = %r" % (tag, value))
			return

		sre = ACTION_TAGCHANGE_RE.match(data)
		if sre:
			entity, tag, value = sre.groups()
			entity = self._parse_entity(entity)
			return

		sre = ACTION_FULLENTITY_RE_1.match(data)
		if not sre:
			sre = ACTION_FULLENTITY_RE_2.match(data)
		if sre:
			entity, cardid = sre.groups()
			entity = self._parse_entity(entity)
			# print("full:", entity, cardid)
			return

		sre = ACTION_SHOWENTITY_RE.match(data)
		if sre:
			entity, cardid = sre.groups()
			entity = self._parse_entity(entity)
			# print("show:", entity, cardid)
			return

		sre = ACTION_HIDEENTITY_RE.match(data)
		if sre:
			entity, tag, value = sre.groups()
			entity = self._parse_entity(entity)
			return

		sre = ACTION_START_RE.match(data)
		if sre:
			entity, blocktype, index, target = sre.groups()
			entity = self._parse_entity(entity)
			target = self._parse_entity(target)

			# print(entity, blocktype, index, target)
			return

		sre = ACTION_METADATA_RE.match(data)
		if sre:
			meta, data, info = sre.groups()
			return

		sre = ACTION_CREATEGAME_RE.match(data)
		if sre:
			id, = sre.groups()
			assert id == "1"
			return

		sre = ACTION_CREATEGAME_PLAYER_RE.match(data)
		if sre:
			id, playerid, account_hi, account_lo = sre.groups()
			return

		if data == "CREATE_GAME":
			# print("<Game>")
			return

		if data == "ACTION_END":
			# print("</Action>")
			return

		print(data)

		pass

	def handle_options(self, timestamp, data):
		sre = OPTIONS_ENTITY_RE.match(data)
		if sre:
			entityid, = sre.groups()
			return

		sre = OPTIONS_OPTION_RE.match(data)
		if sre:
			id, type, entity = sre.groups()
			entity = self._parse_entity(entity)
			return

		sre = OPTIONS_SUBOPTION_RE.match(data)
		if sre:
			subop_type, id, entity = sre.groups()
			entity = self._parse_entity(entity)
			return
		pass

	def toxml(self):
		return ""


def main():
	fname = sys.argv[1]
	parser = PowerLogParser()

	with open(fname, "r") as f:
		parser.read(f)

	print(parser.toxml())


if __name__ == "__main__":
	main()
