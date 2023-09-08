import logging
from typing import Optional

from hearthstone.enums import MetaDataType
from hslog import LogParser
from hslog.packets import (Block, CachedTagForDormantChange, ChangeEntity,
                           Choices, ChosenEntities, CreateGame, FullEntity,
                           HideEntity, MetaData, Options, ResetGame,
                           SendChoices, SendOption, ShowEntity, ShuffleDeck,
                           SubSpell, TagChange, VOSpell)
from hslog.player import coerce_to_entity_id, PlayerManager

from . import elements
from .utils import set_game_meta_on_game


def serialize_entity(entity):
    if entity:
        return coerce_to_entity_id(entity)


def add_initial_tags(ts, packet, packet_element):
    for tag, value in packet.tags:
        tag_element = elements.TagNode(ts, tag, value)
        packet_element.append(tag_element)


def add_choices(ts, packet, packet_element):
    for i, entity_id in enumerate(packet.choices):
        choice_element = elements.ChoiceNode(ts, i, entity_id)
        packet_element.append(choice_element)


def add_options(ts, packet, packet_element):
    for i, option in enumerate(packet.options):
        if option.optype == "option":
            cls = elements.OptionNode
        elif option.optype == "target":
            cls = elements.OptionTargetNode
        elif option.optype == "subOption":
            cls = elements.SubOptionNode
        else:
            raise NotImplementedError("Unhandled option type: %r" % (option.optype))
        try:
            entity = serialize_entity(option.entity)
        except RuntimeError:
            # This is a hack to ensure we can serialize games from Hearthstone 18336.
            # Real names are shoved in the options, not used anywhere else...
            entity = None
        option_element = cls(ts, i, entity, option.error, option.error_param, option.type)
        add_options(ts, option, option_element)
        packet_element.append(option_element)


def add_packets_recursive(packets, entity_element):
    for packet in packets:
        if hasattr(packet, "entity"):
            _ent = serialize_entity(packet.entity)
        ts = packet.ts

        if isinstance(packet, CreateGame):
            packet_element = elements.GameEntityNode(ts, _ent)
            add_initial_tags(ts, packet, packet_element)
            entity_element.append(packet_element)
            for player in packet.players:
                entity_id = serialize_entity(player.entity)
                player_element = elements.PlayerNode(
                    ts, entity_id, player.player_id,
                    player.hi, player.lo, player.name
                )
                entity_element.append(player_element)
                add_initial_tags(ts, player, player_element)
            continue
        elif isinstance(packet, Block):
            effect_index = int(packet.effectindex or 0)
            packet_element = elements.BlockNode(
                ts, _ent, packet.type,
                packet.index if packet.index != -1 else None,
                packet.effectid or None,
                effect_index if effect_index != -1 else None,
                serialize_entity(packet.target),
                packet.suboption if packet.suboption != -1 else None,
                packet.trigger_keyword if packet.trigger_keyword else None
            )
            add_packets_recursive(packet.packets, packet_element)
        elif isinstance(packet, MetaData):
            # With verbose=false, we always have 0 packet.info :(
            if len(packet.info) not in (0, packet.count):
                logging.warning("META_DATA count is %r for %r", packet.count, packet.info)

            if packet.meta == MetaDataType.JOUST:
                data = serialize_entity(packet.data)
            else:
                data = packet.data
            packet_element = elements.MetaDataNode(
                ts, packet.meta, data, packet.count
            )
            for i, info in enumerate(packet.info):
                e = elements.MetaDataInfoNode(packet.ts, i, info)
                packet_element.append(e)
        elif isinstance(packet, TagChange):
            packet_element = elements.TagChangeNode(
                packet.ts, _ent, packet.tag, packet.value,
                packet.has_change_def if packet.has_change_def else None
            )
        elif isinstance(packet, HideEntity):
            packet_element = elements.HideEntityNode(ts, _ent, packet.zone)
        elif isinstance(packet, ShowEntity):
            packet_element = elements.ShowEntityNode(ts, _ent, packet.card_id)
            add_initial_tags(ts, packet, packet_element)
        elif isinstance(packet, FullEntity):
            packet_element = elements.FullEntityNode(ts, _ent, packet.card_id)
            add_initial_tags(ts, packet, packet_element)
        elif isinstance(packet, ChangeEntity):
            packet_element = elements.ChangeEntityNode(ts, _ent, packet.card_id)
            add_initial_tags(ts, packet, packet_element)
        elif isinstance(packet, Choices):
            packet_element = elements.ChoicesNode(
                ts, _ent, packet.id, packet.tasklist, packet.type,
                packet.min, packet.max, serialize_entity(packet.source)
            )
            add_choices(ts, packet, packet_element)
        elif isinstance(packet, SendChoices):
            packet_element = elements.SendChoicesNode(ts, packet.id, packet.type)
            add_choices(ts, packet, packet_element)
        elif isinstance(packet, ChosenEntities):
            packet_element = elements.ChosenEntitiesNode(ts, _ent, packet.id)
            add_choices(ts, packet, packet_element)
        elif isinstance(packet, Options):
            packet_element = elements.OptionsNode(ts, packet.id)
            add_options(ts, packet, packet_element)
        elif isinstance(packet, SendOption):
            packet_element = elements.SendOptionNode(
                ts, packet.option, packet.suboption, packet.target, packet.position
            )
        elif isinstance(packet, ResetGame):
            packet_element = elements.ResetGameNode(ts)
        elif isinstance(packet, SubSpell):
            packet_element = elements.SubSpellNode(
                ts, packet.spell_prefab_guid, packet.source, packet.target_count
            )
            for i, target in enumerate(packet.targets):
                e = elements.SubSpellTargetNode(ts, i, target)
                packet_element.append(e)
            add_packets_recursive(packet.packets, packet_element)
        elif isinstance(packet, CachedTagForDormantChange):
            packet_element = elements.CachedTagForDormantChangeNode(
                packet.ts, _ent, packet.tag, packet.value
            )
        elif isinstance(packet, VOSpell):
            packet_element = elements.VOSpellNode(
                packet.ts, packet.brguid, packet.vospguid, packet.blocking, packet.delayms
            )
        elif isinstance(packet, ShuffleDeck):
            packet_element = elements.ShuffleDeckNode(packet.ts, packet.player_id)
        else:
            raise NotImplementedError(repr(packet))
        entity_element.append(packet_element)


def parse_log(fp, processor, date):
    parser = LogParser()
    parser._game_state_processor = processor
    parser._current_date = date
    parser.read(fp)

    return parser


def game_to_xml(
    tree,
    game_meta=None,
    player_manager: Optional[PlayerManager] = None,
    player_meta=None,
    decks=None
):
    # game_tree = tree.export()
    game_element = elements.GameNode(tree.ts)
    add_packets_recursive(tree.packets, game_element)
    players = game_element.players

    if game_meta is not None:
        set_game_meta_on_game(game_meta, game_element)

    if player_meta is not None:
        for player, meta in zip(players, player_meta):
            player._attributes = meta

    if decks is not None:
        for player, deck in zip(players, decks):
            player.deck = deck

        if player_manager:
            # Set the player names
            for player in players:
                if not player.name:
                    player.name = player_manager.get_player_by_entity_id(player.id).name

    return game_element
