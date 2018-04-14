from datetime import datetime

from hsreplay import elements


TS = datetime(2016, 6, 7)


def test_game_node():
	node = elements.GameNode(TS, None, 1, 2, False)

	assert node.to_xml_string() == (
		'<Game type="1" format="2" scenarioID="false" ts="2016-06-07T00:00:00"/>'
	)


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


def test_player_node_with_deck():
	node = elements.PlayerNode(TS, 2, 1, 144115188075855872, 0, "The Innkeeper")
	node.deck = ["EX1_001", "CS2_231"]
	assert node.to_xml_string() == (
		'<Player id="2" playerID="1" accountHi="144115188075855872" accountLo="0"'
		' name="The Innkeeper">'
		'<Deck><Card id="EX1_001"/><Card id="CS2_231"/></Deck></Player>'
	)


def test_deck_node():
	node = elements.DeckNode(TS)
	assert node.to_xml_string() == "<Deck/>"


def test_card_node():
	node = elements.CardNode(TS, "EX1_001")
	node.to_xml_string() == '<Card id="EX1_001"/>'

	node = elements.CardNode(TS, "EX1_001", True)
	assert node.to_xml_string() == '<Card id="EX1_001" premium="true"/>'


def test_full_entity_node():
	node = elements.FullEntityNode(TS, 4, "EX1_001")
	assert node.to_xml_string() == '<FullEntity id="4" cardID="EX1_001"/>'


def test_show_entity_node():
	node = elements.ShowEntityNode(TS, 4, "EX1_001")
	assert node.to_xml_string() == '<ShowEntity entity="4" cardID="EX1_001"/>'


def test_block_node():
	node = elements.BlockNode(TS, 2, 1)
	assert node.to_xml_string() == '<Block entity="2" type="1" ts="2016-06-07T00:00:00"/>'


def test_meta_data_node():
	node = elements.MetaDataNode(TS, 1, None, 1)
	assert node.to_xml_string() == '<MetaData meta="1" info="1"/>'

	node = elements.MetaDataNode(TS, 1, 2, 1)
	assert node.to_xml_string() == '<MetaData meta="1" data="2" info="1"/>'


def test_meta_data_node_with_info():
	node = elements.MetaDataNode(TS, 1, 2, 1)
	info_node = elements.MetaDataInfoNode(TS, 3, 4)
	node.nodes.append(info_node)
	assert node.to_xml_string() == (
		'<MetaData meta="1" data="2" info="1">'
		'<Info index="3" entity="4"/></MetaData>'
	)


def test_tag_node():
	node = elements.TagNode(TS, 49, 1)
	assert node.to_xml_string() == '<Tag tag="49" value="1"/>'


def test_tag_change_node():
	node = elements.TagChangeNode(TS, 1, 49, 1)
	assert node.to_xml_string() == '<TagChange entity="1" tag="49" value="1"/>'


def test_hide_entity_node():
	node = elements.HideEntityNode(TS, 4, 3)
	assert node.to_xml_string() == '<HideEntity entity="4" zone="3" ts="2016-06-07T00:00:00"/>'


def test_change_entity_node():
	node = elements.ChangeEntityNode(TS, 4, "EX1_001")
	assert node.to_xml_string() == (
		'<ChangeEntity entity="4" cardID="EX1_001" ts="2016-06-07T00:00:00"/>'
	)


def test_choices_node():
	node = elements.ChoicesNode(TS, 2, 1, None, 1, 0, 4, 2)
	assert node.to_xml_string() == (
		'<Choices entity="2" id="1" type="1" min="0" max="4" source="2" ts="2016-06-07T00:00:00"/>'
	)


def test_choice_node():
	node = elements.ChoiceNode(TS, 1, 4)
	assert node.to_xml_string() == '<Choice index="1" entity="4"/>'


def test_chosen_entities_node():
	node = elements.ChosenEntitiesNode(TS, 2, 5)
	assert node.to_xml_string() == '<ChosenEntities entity="2" id="5" ts="2016-06-07T00:00:00"/>'


def test_send_choices_node():
	node = elements.SendChoicesNode(TS, 3, 1)
	assert node.to_xml_string() == '<SendChoices id="3" type="1" ts="2016-06-07T00:00:00"/>'


def test_options_node():
	node = elements.OptionsNode(TS, 1)
	assert node.to_xml_string() == '<Options id="1" ts="2016-06-07T00:00:00"/>'


def test_options_node_with_options():
	node = elements.OptionsNode(TS, 1)
	option_node = elements.OptionNode(TS, 1, 4, None, None, 1)
	node.nodes.append(option_node)

	assert node.to_xml_string() == (
		'<Options id="1" ts="2016-06-07T00:00:00">'
		'<Option index="1" entity="4" type="1"/></Options>'
	)


def test_sub_option_node():
	node = elements.SubOptionNode(TS, 1, 6)
	assert node.to_xml_string() == '<SubOption index="1" entity="6"/>'

	node = elements.SubOptionNode(TS, 1, 6, 1, None)
	assert node.to_xml_string() == '<SubOption index="1" entity="6" error="1"/>'

	node = elements.SubOptionNode(TS, 1, 6, 8, 7)
	assert node.to_xml_string() == '<SubOption index="1" entity="6" error="8" errorParam="7"/>'


def test_option_target_node():
	node = elements.OptionTargetNode(TS, 1, 6)
	assert node.to_xml_string() == '<Target index="1" entity="6"/>'

	node = elements.OptionTargetNode(TS, 1, 6, 1, None)
	assert node.to_xml_string() == '<Target index="1" entity="6" error="1"/>'

	node = elements.OptionTargetNode(TS, 1, 6, 8, 7)
	assert node.to_xml_string() == '<Target index="1" entity="6" error="8" errorParam="7"/>'


def test_send_option_node():
	node = elements.SendOptionNode(TS, 1, 0, 0, -1)
	assert node.to_xml_string() == (
		'<SendOption option="1" subOption="0" target="0" position="-1" ts="2016-06-07T00:00:00"/>'
	)
