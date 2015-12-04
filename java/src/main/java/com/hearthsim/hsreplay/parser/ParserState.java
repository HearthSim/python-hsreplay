package com.hearthsim.hsreplay.parser;

import java.util.Arrays;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import lombok.extern.slf4j.Slf4j;

import com.hearthsim.hsreplay.parser.replaydata.Game;
import com.hearthsim.hsreplay.parser.replaydata.GameData;
import com.hearthsim.hsreplay.parser.replaydata.HearthstoneReplay;
import com.hearthsim.hsreplay.parser.replaydata.gameactions.ChosenEntities;
import com.hearthsim.hsreplay.parser.replaydata.meta.Choices;
import com.hearthsim.hsreplay.parser.replaydata.meta.SendChoices;
import com.hearthsim.hsreplay.parser.replaydata.meta.options.Option;
import com.hearthsim.hsreplay.parser.replaydata.meta.options.Options;

@Getter
@Setter
@ToString
@Slf4j
public class ParserState {

	private HearthstoneReplay replay;
	private Game currentGame;
	private Node node;
	private GameData gameData;
	private SendChoices sendChoices;
	private Choices choices;
	private Options options;
	private Option currentOption;
	private Object lastOption;
	private int firstPlayerId;
	private int currentPlayerId;
	private ChosenEntities currentChosenEntities;

	public ParserState() {
		reset();
	}

	public void reset() {
		replay = new HearthstoneReplay();
		currentGame = new Game();
	}

	public void updateCurrentNode(Class... types) {
		log.info("\t\tUpdating node " + node + " with types " + Arrays.toString(types));
		while (node.getParent() != null && Arrays.asList(types).stream().allMatch(x -> !node.getType().equals(x))) {
			node = node.getParent();
		}
	}

}
