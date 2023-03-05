import filecmp
import tempfile
from io import BytesIO, StringIO
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


def test_game_to_xml_stream_annotations():
    sio = BytesIO()
    with lxml.etree.xmlfile(sio, encoding="utf-8") as xf:
        parser = LogParser()
        with open(logfile("88998_missing_player_hash.power.log")) as f:
            parser.read(f)
            game_meta = {
                "id": 4390995,
                "hs_game_type": 7,
                "format": 2,
                "scenario_id": 2
            }
            player_meta = {
                1: {"rank": 25, "cardback": 157},
                2: {"rank": 24, "cardback": 157},
            }

            with xf.element("HSReplay", attrib={"version": "1.7"}):
                xf.write("\n")
                game_to_xml_stream(
                    parser.games[0],
                    xf,
                    game_meta=game_meta,
                    player_manager=parser.player_manager,
                    player_meta=player_meta,
                )

    lines = StringIO(sio.getvalue().decode("utf-8")).readlines()
    game_line = lines[1]
    player_1_line = lines[17]
    player_2_line = lines[50]

    assert game_line.strip() == (
        '<Game ts="20:24:43.065598" id="4390995" format="2" type="7" scenarioID="2">'
    )

    assert player_1_line.strip() == (
        '<Player id="2" playerID="1" accountHi="144115193835963207" '
        'accountLo="66765537" cardback="157" rank="25">'
    )

    assert player_2_line.strip() == (
        '<Player id="3" playerID="2" accountHi="144115193835963207" accountLo="28673911" '
        'cardback="157" rank="24">'
    )
