import logging
from hearthstone import hslog
from hearthstone.enums import MetaDataType
from .elements import *


def serialize_entity(entity):
	if entity:
		e = int(entity)
		if e:
			return e


def add_initial_tags(ts, packet, packet_element):
	for tag, value in packet.tags:
		tag_element = TagNode(ts, tag, value)
		packet_element.append(tag_element)


def add_choices(ts, packet, packet_element):
	for i, entity_id in enumerate(packet.choices):
		choice_element = ChoiceNode(ts, i, entity_id)
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
		entity = serialize_entity(option.entity)
		option_element = cls(ts, i, entity, option.type)
		add_options(ts, option, option_element)
		packet_element.append(option_element)


def add_packets_recursive(packets, entity_element):
	for packet in packets:
		if hasattr(packet, "entity"):
			_ent = serialize_entity(packet.entity)
		ts = packet.ts

		if isinstance(packet, hslog.packets.CreateGame):
			packet_element = GameEntityNode(ts, _ent)
			add_initial_tags(ts, packet, packet_element)
			entity_element.append(packet_element)
			for player in packet.players:
				entity_id = serialize_entity(player.entity)
				player_element = PlayerNode(
					ts, entity_id, player.player_id,
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
			add_packets_recursive(packet.packets, packet_element)
		elif isinstance(packet, hslog.packets.MetaData):
			# With verbose=false, we always have 0 packet.info :(
			if len(packet.info) not in (0, packet.count):
				logging.warning("META_DATA count is %r for %r", packet.count, packet.info)

			if packet.meta == MetaDataType.JOUST:
				data = serialize_entity(packet.data)
			else:
				data = packet.data
			packet_element = MetaDataNode(
				ts, packet.meta, data, packet.count
			)
			for i, info in enumerate(packet.info):
				e = MetaDataInfoNode(packet.ts, i, info)
				packet_element.append(e)
		elif isinstance(packet, hslog.packets.TagChange):
			packet_element = TagChangeNode(
				packet.ts, _ent, packet.tag, packet.value
			)
		elif isinstance(packet, hslog.packets.HideEntity):
			packet_element = HideEntityNode(ts, _ent, packet.zone)
		elif isinstance(packet, hslog.packets.ShowEntity):
			packet_element = ShowEntityNode(ts, _ent, packet.card_id)
			add_initial_tags(ts, packet, packet_element)
		elif isinstance(packet, hslog.packets.FullEntity):
			packet_element = FullEntityNode(ts, _ent, packet.card_id)
			add_initial_tags(ts, packet, packet_element)
		elif isinstance(packet, hslog.packets.ChangeEntity):
			packet_element = ChangeEntityNode(ts, _ent, packet.card_id)
			add_initial_tags(ts, packet, packet_element)
		elif isinstance(packet, hslog.packets.Choices):
			packet_element = ChoicesNode(
				ts, _ent, packet.id, packet.tasklist, packet.type,
				packet.min, packet.max, serialize_entity(packet.source)
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


def game_to_xml(tree, game_meta=None, player_meta=None, decks=None):
	game_tree = tree.export()
	game_element = GameNode(tree.ts)
	add_packets_recursive(tree.packets, game_element)
	players = game_element.players

	if game_meta is not None:
		game_element._attributes = game_meta

	if player_meta is not None:
		for player, meta in zip(players, player_meta):
			player._attributes = meta

	if decks is not None:
		for player, deck in zip(players, decks):
			player.deck = deck

	# Set the player names
	for player in players:
		if not player.name:
			player.name = tree.manager.get_player_by_id(player.id).name

	return game_element
