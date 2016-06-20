from hsreplay import DTD_VERSION
from .dumper import game_to_xml, parse_log
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
		root = ret._create_document()

		for game in parser.games:
			root.append(game_to_xml(game))

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

	def to_xml(self, pretty=False):
		if self.root is None:
			raise ValueError("HSReplayDocument is uninitialized and empty.")

		return toxml(self.root, pretty=pretty)
