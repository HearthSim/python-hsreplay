package info.hearthsim.hsreplay.parser;

import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import info.hearthsim.hsreplay.enums.GameType;
import info.hearthsim.hsreplay.parser.handlers.DataHandler;
import info.hearthsim.hsreplay.parser.handlers.OptionsHandler;
import info.hearthsim.hsreplay.parser.replaydata.Game;
import info.hearthsim.hsreplay.parser.replaydata.HearthstoneReplay;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ReplayParser {

	public static final String VERSION = "1.0";
	public static final int HEARTHSTONE_BUILD = 10833;

	private final ParserState state = new ParserState();

	public HearthstoneReplay fromString(Iterable<String> lines, GameType... gameTypes) throws Exception {
		return fromString(lines, HEARTHSTONE_BUILD, gameTypes);
	}

	public HearthstoneReplay fromString(Iterable<String> lines, int hsBuild, GameType... gameTypes) throws Exception {
		read(lines);
		state.getReplay().setVersion(VERSION);
		state.getReplay().setBuild(String.valueOf(hsBuild));
		for (int i = 0; i < state.getReplay().getGames().size(); i++) {
			if (gameTypes.length == 1) {
				state.getReplay().getGames().get(i).setType(gameTypes[0].getIntValue());
			}
			else {
				state.getReplay().getGames().get(i).setType(gameTypes.length > i ? gameTypes[i].getIntValue() : 0);
			}
		}
		return state.getReplay();
	}

	private void read(Iterable<String> lines) throws Exception {
		state.reset();
		state.getReplay().setGames(new ArrayList<Game>());
		Pattern logTypeRegex = null;

		for (String line : lines) {

			log.debug("Considering input log line: " + line);
			Matcher match = null;
			if (logTypeRegex == null) {
				match = Regexes.PowerlogLineRegex.matcher(line);
				if (match.matches()) {
					log.debug("\tMatching PowerlogLineRegex");
					logTypeRegex = Regexes.PowerlogLineRegex;
				}
				else {
					match = Regexes.OutputlogLineRegex.matcher(line);
					if (match.matches()) {
						log.debug("\tMatching OutputLineRegex");
						logTypeRegex = Regexes.OutputlogLineRegex;
					}
					else {
						log.debug("\tNot matching any regex " + line);
					}
				}
			}
			else {
				match = logTypeRegex.matcher(line);
			}

			if (!match.matches()) {
				continue;
			}

			addData(match.group(1), match.group(2), match.group(3));
		}
	}

	private void addData(String timestamp, String method, String data) throws Exception {

		switch (method) {
			case "GameState.DebugPrintPower":
				DataHandler.handle(timestamp, data, state);
				break;
			// case "PowerTaskList.DebugPrintPower":
			// DataHandler.handle(timestamp, data, state);
			// break;
			// case "GameState.SendChoices":
			// SendChoicesHandler.handle(timestamp, data, state);
			// break;
			// case "GameState.DebugPrintChoices":
			// case "GameState.DebugPrintEntityChoices":
			// ChoicesHandler.handle(timestamp, data, state);
			// break;
			// case "GameState.DebugPrintEntitiesChosen":
			// EntityChosenHandler.handle(timestamp, data, state);
			// break;
			case "GameState.DebugPrintOptions":
				OptionsHandler.handle(timestamp, data, state);
				break;
			// case "GameState.SendOption":
			// SendOptionHandler.handle(timestamp, data, state);
			// break;
			// case "GameState.OnEntityChoices":
			// // Spectator mode noise
			// break;
			// case "ChoiceCardMgr.WaitThenShowChoices":
			// // Not needed for replays
			// break;
			// case "GameState.DebugPrintChoice":
			// System.out.println("Warning: DebugPrintChoice was removed in
			// 10357. Ignoring.");
			// break;
			default:
				if (!method.startsWith("PowerTaskList.") && !method.startsWith("PowerProcessor.")
						&& !method.startsWith("PowerSpellController")) {
					log.warn("Warning: Unhandled method: " + method);
				}
				break;
		}
	}
}
