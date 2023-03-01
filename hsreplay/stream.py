import logging
from contextlib import contextmanager
from typing import Optional

from hearthstone.enums import MetaDataType
from hslog.packets import (Block, CachedTagForDormantChange, ChangeEntity,
                           Choices, ChosenEntities, CreateGame, FullEntity,
                           HideEntity, MetaData, Options, ResetGame,
                           SendChoices, SendOption, ShowEntity, ShuffleDeck,
                           SubSpell, TagChange, VOSpell)
from hslog.player import PlayerManager, PlayerReference

from . import elements
from .dumper import serialize_entity


@contextmanager
def element_context(xf, elt: elements.Node):
    attributes = {}
    for attr in elt.attributes:
        attrib = getattr(elt, attr, None)
        if attrib is not None:
            if isinstance(attrib, bool):
                attrib = str(attrib).lower()
            elif isinstance(attrib, int):
                # Check for enums
                attrib = str(int(attrib))
            elif isinstance(attrib, PlayerReference):
                attrib = str(attrib.entity_id)
            attributes[attr] = attrib
    if elt.timestamp and elt.ts:
        attributes["ts"] = elt.ts.isoformat()

    for k, v in elt._attributes.items():
        attributes[k] = v

    with xf.element(elt.tagname, attrib=attributes):
        yield


def write_element(xf, elt: elements.Node):
    xf.write(elt.xml())


def write_initial_tags(xf, ts, packet):
    for tag, value in packet.tags:
        write_element(xf, elements.TagNode(ts, tag, value))


def write_choices(xf, ts, packet):
    for i, entity_id in enumerate(packet.choices):
        write_element(xf, elements.ChoiceNode(ts, i, entity_id))


def write_options(xf, ts, packet):
    for i, option in enumerate(packet.options):
        if option.optype == "option":
            cls = elements.OptionNode
        elif option.optype == "target":
            cls = elements.OptionTargetNode
        elif option.optype == "subOption":
            cls = elements.SubOptionNode
        else:
            raise NotImplementedError("Unhandled option type: %r" % option.optype)
        try:
            entity = serialize_entity(option.entity)
        except RuntimeError:
            # This is a hack to ensure we can serialize games from Hearthstone 18336.
            # Real names are shoved in the options, not used anywhere else...
            entity = None
        option_element = cls(ts, i, entity, option.error, option.error_param, option.type)
        with element_context(xf, option_element.tagname):

            # Handle suboptions

            write_options(xf, ts, option)


def write_packets_recursive(xf, packets):
    for packet in packets:
        if hasattr(packet, "entity"):
            _ent = serialize_entity(packet.entity)
        ts = packet.ts

        if isinstance(packet, CreateGame):
            game_element = elements.GameEntityNode(ts, _ent)
            with element_context(xf, game_element):
                write_initial_tags(xf, ts, packet)

            for player in packet.players:
                entity_id = serialize_entity(player.entity)
                player_element = elements.PlayerNode(
                    ts, entity_id, player.player_id,
                    player.hi, player.lo, player.name
                )
                with element_context(xf, player_element):
                    write_initial_tags(xf, ts, player)
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
            with element_context(xf, packet_element):
                write_packets_recursive(xf, packet.packets)
        elif isinstance(packet, MetaData):
            # With verbose=false, we always have 0 packet.info :(
            if len(packet.info) not in (0, packet.count):
                logging.warning("META_DATA count is %r for %r", packet.count, packet.info)

            if packet.meta == MetaDataType.JOUST:
                data = serialize_entity(packet.data)
            else:
                data = packet.data

            metadata_element = elements.MetaDataNode(ts, packet.meta, data, packet.count)
            with element_context(xf, metadata_element):
                for i, info in enumerate(packet.info):
                    write_element(xf, elements.MetaDataInfoNode(packet.ts, i, info))
        elif isinstance(packet, TagChange):
            write_element(
                xf,
                elements.TagChangeNode(
                    packet.ts, _ent, packet.tag, packet.value,
                    packet.has_change_def if packet.has_change_def else None
                )
            )
        elif isinstance(packet, HideEntity):
            write_element(xf, elements.HideEntityNode(ts, _ent, packet.zone))
        elif isinstance(packet, ShowEntity):
            with element_context(xf, elements.ShowEntityNode(ts, _ent, packet.card_id)):
                write_initial_tags(xf, ts, packet)
        elif isinstance(packet, FullEntity):
            with element_context(xf, elements.FullEntityNode(ts, _ent, packet.card_id)):
                write_initial_tags(xf, ts, packet)
        elif isinstance(packet, ChangeEntity):
            with element_context(xf, elements.ChangeEntityNode(ts, _ent, packet.card_id)):
                write_initial_tags(xf, ts, packet)
        elif isinstance(packet, Choices):
            with element_context(
                xf,
                elements.ChoicesNode(
                    ts, _ent, packet.id, packet.tasklist, packet.type,
                    packet.min, packet.max, serialize_entity(packet.source)
                )
            ):
                write_choices(xf, ts, packet)
        elif isinstance(packet, SendChoices):
            with element_context(xf, elements.SendChoicesNode(ts, packet.id, packet.type)):
                write_choices(xf, ts, packet)
        elif isinstance(packet, ChosenEntities):
            with element_context(xf, elements.ChosenEntitiesNode(ts, _ent, packet.id)):
                write_choices(xf, ts, packet)
        elif isinstance(packet, Options):
            with element_context(xf, elements.OptionsNode(ts, packet.id)):
                write_options(xf, ts, packet)
        elif isinstance(packet, SendOption):
            write_element(
                xf,
                elements.SendOptionNode(
                    ts, packet.option, packet.suboption, packet.target, packet.position
                )
            )
        elif isinstance(packet, ResetGame):
            write_element(xf, elements.ResetGameNode(ts))
        elif isinstance(packet, SubSpell):
            with element_context(
                xf,
                elements.SubSpellNode(
                    ts, packet.spell_prefab_guid, packet.source, packet.target_count
                )
            ):
                for i, target in enumerate(packet.targets):
                    write_element(xf, elements.SubSpellTargetNode(ts, i, target))
                write_packets_recursive(xf, packet.packets)
        elif isinstance(packet, CachedTagForDormantChange):
            write_element(
                xf,
                elements.CachedTagForDormantChangeNode(
                    packet.ts, _ent, packet.tag, packet.value
                )
            )
        elif isinstance(packet, VOSpell):
            write_element(
                xf,
                elements.VOSpellNode(
                    packet.ts,
                    packet.brguid,
                    packet.vospguid,
                    packet.blocking,
                    packet.delayms
                )
            )
        elif isinstance(packet, ShuffleDeck):
            write_element(xf, elements.ShuffleDeckNode(packet.ts, packet.player_id))
        else:
            raise NotImplementedError(repr(packet))


def game_to_xml_stream(
    tree,
    xf,
    game_meta=None,
    player_manager: Optional[PlayerManager] = None,
    player_meta=None,
    decks=None
):
    game_element = elements.GameNode(tree.ts)
    players = game_element.players

    if game_meta is not None:
        game_element._attributes = game_meta

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

    with element_context(xf, game_element):
        write_packets_recursive(xf, tree.packets)
