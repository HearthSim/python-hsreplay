package info.hearthsim.hsreplay.parser.handlers;

import info.hearthsim.hsreplay.enums.ChoiceType;
import info.hearthsim.hsreplay.parser.Helper;
import info.hearthsim.hsreplay.parser.ParserState;
import info.hearthsim.hsreplay.parser.Regexes;
import info.hearthsim.hsreplay.parser.replaydata.Game;
import info.hearthsim.hsreplay.parser.replaydata.gameactions.Action;
import info.hearthsim.hsreplay.parser.replaydata.meta.Choice;
import info.hearthsim.hsreplay.parser.replaydata.meta.Choices;

import java.util.ArrayList;
import java.util.regex.Matcher;

public class ChoicesHandler {

	public static void handle(String timestamp, String data, ParserState state) throws Exception {
		data = data.trim();
		Matcher match = Regexes.ChoicesChoiceRegex_OLD.matcher(data);
		if (match.matches()) {
			String rawEntity = match.group(1);
			String playerId = match.group(2);
			String rawType = match.group(3);
			String min = match.group(4);
			String max = match.group(5);
			int entity = Helper.parseEntity(rawEntity, state);
			int type = ChoiceType.parseEnum(rawType);

			Choices choices = Choices.builder().choiceList(new ArrayList<Choice>()).entity(entity)
					.max(Integer.parseInt(max)).min(Integer.parseInt(min)).playerId(Integer.parseInt(playerId))
					.type(type).build();
			choices.setTimestamp(timestamp);
			state.setChoices(choices);

			if (state.getNode().getType().isAssignableFrom(Game.class)) {
				((Game) state.getNode().getObject()).getData().add(state.getChoices());
			}
			else if (state.getNode().getType().isAssignableFrom(Action.class)) {
				((Action) state.getNode().getObject()).getData().add(state.getChoices());
			}
			else {
				throw new Exception("Invalid node " + state.getNode().getType() + " -- " + data);
			}
			return;
		}

		match = Regexes.ChoicesChoiceRegex.matcher(data);
		if (match.matches()) {
			// NOTE: in 10357, "Player" is bugged, it's treating a player ID
			// as an entity ID, resulting in "Player=GameEntity"
			// For our own sanity we keep the old playerID logic from the
			// previous builds, we'll change to "player" when it's fixed.
			String rawEntity = match.group(1);
			String rawPlayer = match.group(2);
			String taskList = match.group(3);
			String rawType = match.group(4);
			String min = match.group(5);
			String max = match.group(6);

			int entity = Helper.parseEntity(rawEntity, state);
			int player = Helper.parseEntity(rawPlayer, state);
			int type = ChoiceType.parseEnum(rawType);

			Choices choices = Choices.builder().choiceList(new ArrayList<Choice>()).entity(entity)
					.max(Integer.parseInt(max)).min(Integer.parseInt(min)).playerId(player).type(type)
					.taskList(Integer.parseInt(taskList)).build();
			choices.setTimestamp(timestamp);
			state.setChoices(choices);

			if (state.getNode().getType().isAssignableFrom(Game.class)) {
				((Game) state.getNode().getObject()).getData().add(state.getChoices());
			}
			else if (state.getNode().getType().isAssignableFrom(Action.class)) {
				((Action) state.getNode().getObject()).getData().add(state.getChoices());
			}
			else {
				throw new Exception("Invalid node " + state.getNode().getType() + " -- " + data);
			}
			return;
		}

		match = Regexes.ChoicesSourceRegex.matcher(data);
		if (match.matches()) {
			String rawEntity = match.group(1);
			int entity = Helper.parseEntity(rawEntity, state);
			state.getChoices().setSource(entity);
			return;
		}

		match = Regexes.ChoicesEntitiesRegex.matcher(data);
		if (match.matches()) {
			String index = match.group(1);
			String rawEntity = match.group(2);
			int entity = Helper.parseEntity(rawEntity, state);
			Choice choice = new Choice(entity, Integer.parseInt(index));
			state.getChoices().getChoiceList().add(choice);
		}
	}
}
