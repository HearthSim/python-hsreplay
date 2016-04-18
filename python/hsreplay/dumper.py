from hearthstone import hslog
from xml.etree import ElementTree
from . import __version__
from .elements import *
from .utils import pretty_xml


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
	if isinstance(entity, str):
		return entity
	elif entity:
		return entity.id


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
		elif isinstance(packet, hslog.packets.Action):
			packet_element = ActionNode(
				ts, _ent, packet.type,
				packet.index if packet.index != -1 else None,
				serialize_entity(packet.target)
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


def parse_log(fp, processor="GameState", date=None):
	parser = hslog.LogWatcher()
	parser._game_state_processor = processor
	parser._current_date = date
	parser.read(fp)

	return parser


def packet_tree_to_xml(parser):
	builder = ElementTree.TreeBuilder()
	builder.start("HSReplay", {"version": __version__})
	builder.end("HSReplay")
	root = builder.close()

	for game in parser.games:
		game_element = GameNode(game.ts)
		add_packets_recursive(game, game_element)
		root.append(game_element.xml())

	return root


def log_to_xml(fp, *args, **kwargs):
	parser = parse_log(fp, *args, **kwargs)
	root = packet_tree_to_xml(parser)
	return pretty_xml(root)
