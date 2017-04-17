from datetime import datetime
from hsreplay import elements


TS = datetime(2016, 6, 7)


def test_game_entity_node():
	node = elements.GameEntityNode(TS, 1)

	assert node.to_xml_string() == '<GameEntity id="1"/>'


def test_player_node():
	node = elements.PlayerNode(TS, 2, 1, 144115188075855872, 0, "The Innkeeper")
	assert node.to_xml_string() == (
		'<Player id="2" playerID="1" accountHi="144115188075855872" accountLo="0"'
		' name="The Innkeeper"/>'
	)

	node = elements.PlayerNode(TS, 3, 2, 144115193835963207, 0, "Player One", 0, None, 62)
	assert node.to_xml_string() == (
		'<Player id="3" playerID="2" accountHi="144115193835963207" accountLo="0"'
		' name="Player One" rank="0" cardback="62"/>'
	)
