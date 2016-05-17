from hearthstone import hslog
from . import __version__
from .elements import *
from .utils import ElementTree, toxml


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


def serialize_entity(entity):
	if isinstance(entity, hslog.entities.Entity):
		return entity.id
	elif entity:
		return entity


def add_packets_recursive(entity, entity_element):
	for packet in entity:
		_ent = serialize_entity(packet.entity)
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
		elif isinstance(packet, hslog.packets.Block):
			packet_element = BlockNode(
				ts, _ent, packet.type,
				packet.index if packet.index != -1 else None,
				serialize_entity(packet.target)
			)
			add_packets_recursive(packet, packet_element)
		elif isinstance(packet, hslog.packets.MetaData):
			# With verbose=false, we always have 0 packet.info :(
			assert len(packet.info) in (0, packet.count)
			packet_element = MetaDataNode(
				ts, packet.type, _ent, packet.count
			)
			for i, info in enumerate(packet.info):
				id = info and info.id or 0
				e = MetaDataInfoNode(packet.ts, i, id)
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
		elif isinstance(packet, hslog.packets.ChangeEntity):
			packet_element = ChangeEntityNode(ts, _ent, packet.cardid)
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


def parse_log(fp, processor, date):
	parser = hslog.LogParser()
	parser._game_state_processor = processor
	parser._current_date = date
	parser.read(fp)

	return parser


def create_document(version, build):
	builder = ElementTree.TreeBuilder()
	attrs = {"version": version}
	if build is not None:
		attrs["build"] = str(build)
	builder.start("HSReplay", attrs)
	builder.end("HSReplay")

	return builder.close()


def game_to_xml(game, game_meta=None, player_meta=None, decks=None):
	game_element = GameNode(game.ts)
	add_packets_recursive(game, game_element)
	players = game_element.nodes[1:3]

	if game_meta is not None:
		game_element._attributes = game_meta

	if player_meta is not None:
		for player, meta in zip(players, player_meta):
			player._attributes = meta

	if decks is not None:
		for player, deck in zip(players, decks):
			player.deck = deck

	return game_element.xml()


def log_to_xml(fp, processor="GameState", date=None, version=__version__, build=None, pretty=False):
	root = create_document(version, build)
	parser = parse_log(fp, processor, date)
	for game in parser.games:
		root.append(game_to_xml(game))

	return toxml(root, pretty)
