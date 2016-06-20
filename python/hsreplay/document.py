from hsreplay import DTD_VERSION
from .dumper import game_to_xml, parse_log
from .elements import GameNode
from .utils import ElementTree, toxml


class HSReplayDocument:
	ROOT_NAME = "HSReplay"

	@classmethod
	def from_log_file(cls, fp, processor="GameState", date=None, build=None):
		parser = parse_log(fp, processor, date)
		return cls.from_parser(parser, build)

	@classmethod
	def from_parser(cls, parser, build=None):
		ret = cls(build)
		ret._update_document()

		for game in parser.games:
			gamenode = game_to_xml(game)
			ret.games.append(gamenode)

		return ret

	@classmethod
	def from_xml_file(cls, fp):
		xml = ElementTree.parse(fp)
		return cls.from_xml(xml)

	@classmethod
	def from_xml(cls, xml):
		root = xml.getroot()
		build = root.attrib.get("build")
		ret = cls(build)
		ret.version = root.attrib.get("version")
		for game in xml.findall("Game"):
			gamenode = GameNode.from_xml(game)
			ret.games.append(gamenode)

		return ret

	def __init__(self, build=None):
		self.build = build
		self.version = DTD_VERSION
		self.games = []
		self.root = None

	def _create_document(self):
		builder = ElementTree.TreeBuilder()
		attrs = {"version": self.version}
		if self.build is not None:
			attrs["build"] = str(self.build)
		builder.start(self.ROOT_NAME, attrs)
		builder.end(self.ROOT_NAME)

		self.root = builder.close()
		return self.root

	def _update_document(self):
		if self.root is None:
			self._create_document()

		for game in self.games:
			self.root.append(game.xml())

	def to_xml(self, pretty=False):
		self._update_document()
		return toxml(self.root, pretty=pretty)
