import filecmp
import tempfile
from typing import Optional, Type

import lxml
from hslog import LogParser
from hslog.filter import BattlegroundsLogFilter

from hsreplay import SYSTEM_DTD
from hsreplay.document import HSReplayDocument
from hsreplay.stream import game_to_xml_stream
from tests.conftest import logfile


def assert_game_to_xml_equal(
    logname: str,
    log_filter_cls: Optional[Type[BattlegroundsLogFilter]] = None
):
    parser = LogParser()
    with open(logname) as f:
        if log_filter_cls is not None:
            parser.read(log_filter_cls(f))
        else:
            parser.read(f)

    with (
        tempfile.NamedTemporaryFile() as t1,
        tempfile.NamedTemporaryFile(mode="w+") as t2
    ):
        with lxml.etree.xmlfile(t1, encoding="utf-8") as xf:
            xf.write_declaration()
            xf.write_doctype('<!DOCTYPE hsreplay SYSTEM "%s">' % SYSTEM_DTD),

            with xf.element("HSReplay", attrib={"version": "1.7"}):
                xf.write("\n")
                for game in parser.games:
                    game_to_xml_stream(game, xf, indent=2)

            xf.flush()
            t1.write(b"\n")
            t1.flush()

        doc = HSReplayDocument.from_packet_tree(parser.games)
        xml = doc.to_xml(pretty=True)
        t2.write(xml)
        t2.flush()

        assert filecmp.cmp(t1.name, t2.name, shallow=False)


def test_game_to_xml_stream_compat_hearthstone():
    assert_game_to_xml_equal(logfile("88998_missing_player_hash.power.log"))


def test_game_to_xml_stream_compat_battlegrounds():
    assert_game_to_xml_equal(
        logfile("139963_battlegrounds_perfect_game.power.log"),
        log_filter_cls=BattlegroundsLogFilter
    )


def test_game_to_xml_stream_compat_mercenaries():
    assert_game_to_xml_equal(logfile("93227_mercenaries_solo_bounty.power.log"))
