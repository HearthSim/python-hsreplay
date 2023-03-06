import logging
from contextlib import contextmanager
from typing import Dict, Optional

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
def element_context(xf, elt: elements.Node, indent: int = 0):
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

    xf.write(" " * indent)

    with xf.element(elt.tagname, attrib=attributes):
        xf.write("\n")
        yield
        xf.write(" " * indent)

    xf.write("\n")


def write_element(xf, elt: elements.Node, indent: int = 0):
    xf.write(" " * indent)
    xf.write(elt.xml())
    xf.write("\n")


def write_initial_tags(xf, ts, packet, indent: int = 0):
    for tag, value in packet.tags:
        write_element(xf, elements.TagNode(ts, tag, value), indent=indent)


def write_choices(xf, ts, packet, indent: int = 0):
    for i, entity_id in enumerate(packet.choices):
        write_element(xf, elements.ChoiceNode(ts, i, entity_id), indent=indent)


def write_options(xf, ts, packet, indent: int = 0):
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

        if option.options:
            with element_context(xf, option_element, indent=indent):

                # Handle suboptions

                write_options(xf, ts, option, indent=indent + 2)
        else:
            write_element(xf, option_element, indent=indent)


def write_deck(xf, ts, deck, indent: int = 0):
    with element_context(xf, elements.DeckNode(ts), indent=indent):
        for card in deck:
            write_element(xf, elements.CardNode(ts, card), indent=indent + 2)


def write_player(
    xf,
    ts,
    player,
    indent: int = 0,
    player_manager: Optional[PlayerManager] = None,
    player_meta: Optional[Dict] = None
):
    entity_id = serialize_entity(player.entity)
    player_element = elements.PlayerNode(
        ts, entity_id, player.player_id, player.hi, player.lo, player.name
    )

    this_player_meta = {}
    if player_meta and player.player_id in player_meta:
        this_player_meta = player_meta.pop(player.player_id)

    if this_player_meta.get("cardback") is not None:
        player_element._attributes["cardback"] = str(this_player_meta["cardback"])
    if this_player_meta.get("legendRank") is not None:
        player_element._attributes["legendRank"] = str(this_player_meta["legend_rank"])
    if this_player_meta.get("rank") is not None:
        player_element._attributes["rank"] = str(this_player_meta["rank"])

    if player_manager:
        if not hasattr(player_element, "name"):
            player_record = player_manager.get_player_by_entity_id(entity_id)
            player_element._attributes["name"] = player_record.name

    with element_context(xf, player_element, indent=indent):
        if this_player_meta.get("deck") is not None:
            write_deck(xf, ts, this_player_meta["deck"], indent=indent + 2)
        write_initial_tags(xf, ts, player, indent=indent + 2)


def write_packets_recursive(
    xf,
    packets,
    indent: int = 0,
    player_manager: Optional[PlayerManager] = None,
    player_meta: Optional[Dict] = None
):
    for packet in packets:
        if hasattr(packet, "entity"):
            _ent = serialize_entity(packet.entity)
        ts = packet.ts

        if isinstance(packet, CreateGame):
            game_element = elements.GameEntityNode(ts, _ent)
            with element_context(xf, game_element, indent=indent):
                write_initial_tags(xf, ts, packet, indent=indent + 2)

            for player in packet.players:
                write_player(
                    xf,
                    ts,
                    player,
                    indent=indent,
                    player_manager=player_manager,
                    player_meta=player_meta
                )
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
            if packet.packets:
                with element_context(xf, packet_element, indent=indent):
                    write_packets_recursive(
                        xf,
                        packet.packets,
                        indent=indent + 2,
                        player_manager=player_manager,
                        player_meta=player_meta
                    )
            else:
                write_element(xf, packet_element, indent=indent)
        elif isinstance(packet, MetaData):
            # With verbose=false, we always have 0 packet.info :(
            if len(packet.info) not in (0, packet.count):
                logging.warning("META_DATA count is %r for %r", packet.count, packet.info)

            if packet.meta == MetaDataType.JOUST:
                data = serialize_entity(packet.data)
            else:
                data = packet.data

            metadata_element = elements.MetaDataNode(ts, packet.meta, data, packet.count)
            if packet.info:
                with element_context(xf, metadata_element, indent=indent):
                    for i, info in enumerate(packet.info):
                        write_element(
                            xf,
                            elements.MetaDataInfoNode(packet.ts, i, info),
                            indent=indent + 2
                        )
            else:
                write_element(xf, metadata_element, indent=indent)
        elif isinstance(packet, TagChange):
            write_element(
                xf,
                elements.TagChangeNode(
                    packet.ts, _ent, packet.tag, packet.value,
                    packet.has_change_def if packet.has_change_def else None
                ),
                indent=indent
            )
        elif isinstance(packet, HideEntity):
            write_element(xf, elements.HideEntityNode(ts, _ent, packet.zone), indent=indent)
        elif isinstance(packet, ShowEntity):
            with element_context(
                xf,
                elements.ShowEntityNode(ts, _ent, packet.card_id),
                indent=indent
            ):
                write_initial_tags(xf, ts, packet, indent=indent + 2)
        elif isinstance(packet, FullEntity):
            with element_context(
                xf,
                elements.FullEntityNode(ts, _ent, packet.card_id),
                indent=indent
            ):
                write_initial_tags(xf, ts, packet, indent=indent + 2)
        elif isinstance(packet, ChangeEntity):
            with element_context(
                xf,
                elements.ChangeEntityNode(ts, _ent, packet.card_id),
                indent=indent
            ):
                write_initial_tags(xf, ts, packet, indent=indent + 2)
        elif isinstance(packet, Choices):
            with element_context(
                xf,
                elements.ChoicesNode(
                    ts, _ent, packet.id, packet.tasklist, packet.type,
                    packet.min, packet.max, serialize_entity(packet.source)
                ),
                indent=indent
            ):
                write_choices(xf, ts, packet, indent=indent + 2)
        elif isinstance(packet, SendChoices):
            with element_context(
                xf,
                elements.SendChoicesNode(ts, packet.id, packet.type),
                indent=indent
            ):
                write_choices(xf, ts, packet, indent=indent + 2)
        elif isinstance(packet, ChosenEntities):
            with element_context(
                xf,
                elements.ChosenEntitiesNode(ts, _ent, packet.id),
                indent=indent
            ):
                write_choices(xf, ts, packet, indent=indent + 2)
        elif isinstance(packet, Options):
            with element_context(xf, elements.OptionsNode(ts, packet.id), indent=indent):
                write_options(xf, ts, packet, indent=indent + 2)
        elif isinstance(packet, SendOption):
            write_element(
                xf,
                elements.SendOptionNode(
                    ts, packet.option, packet.suboption, packet.target, packet.position
                ),
                indent=indent
            )
        elif isinstance(packet, ResetGame):
            write_element(xf, elements.ResetGameNode(ts), indent=indent)
        elif isinstance(packet, SubSpell):
            subspell_elements = elements.SubSpellNode(
                ts, packet.spell_prefab_guid, packet.source, packet.target_count
            )
            if packet.packets or packet.targets:
                with element_context(xf, subspell_elements, indent=indent):
                    for i, target in enumerate(packet.targets):
                        write_element(
                            xf,
                            elements.SubSpellTargetNode(ts, i, target),
                            indent=indent + 2
                        )
                    write_packets_recursive(
                        xf,
                        packet.packets,
                        indent=indent + 2,
                        player_manager=player_manager,
                        player_meta=player_meta,
                    )
            else:
                write_element(xf, subspell_elements, indent=indent)
        elif isinstance(packet, CachedTagForDormantChange):
            write_element(
                xf,
                elements.CachedTagForDormantChangeNode(
                    packet.ts, _ent, packet.tag, packet.value
                ),
                indent=indent
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
                ),
                indent=indent
            )
        elif isinstance(packet, ShuffleDeck):
            write_element(
                xf,
                elements.ShuffleDeckNode(packet.ts, packet.player_id),
                indent=indent
            )
        else:
            raise NotImplementedError(repr(packet))


def game_to_xml_stream(
    tree,
    xf,
    game_meta: Optional[Dict] = None,
    player_manager: Optional[PlayerManager] = None,
    player_meta: Optional[Dict] = None,
    indent: int = 0,
):
    game_element = elements.GameNode(tree.ts)

    if game_meta is not None:
        if game_meta.get("id") is not None:
            game_element._attributes["id"] = str(game_meta["id"])
        if game_meta.get("format") is not None:
            game_element._attributes["format"] = str(game_meta["format"])
        if game_meta.get("hs_game_type") is not None:
            game_element._attributes["type"] = str(game_meta["hs_game_type"])
        if game_meta.get("scenario_id") is not None:
            game_element._attributes["scenarioID"] = str(game_meta["scenario_id"])

        if "reconnecting" in game_meta:
            game_element._attributes["reconnecting"] = str(game_meta["reconnecting"])

    with element_context(xf, game_element, indent=indent):
        write_packets_recursive(
            xf,
            tree.packets,
            player_manager=player_manager,
            player_meta=player_meta,
            indent=indent + 2
        )
