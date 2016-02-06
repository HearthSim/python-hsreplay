package info.hearthsim.hsreplay.parser.handlers;

import info.hearthsim.hsreplay.parser.Helper;
import info.hearthsim.hsreplay.parser.ParserState;
import info.hearthsim.hsreplay.parser.Regexes;
import info.hearthsim.hsreplay.parser.replaydata.gameactions.ChosenEntities;
import info.hearthsim.hsreplay.parser.replaydata.meta.Choice;

import java.util.ArrayList;
import java.util.regex.Matcher;

import lombok.extern.slf4j.Slf4j;

@Slf4j
public class EntityChosenHandler {

	public static void handle(String timestamp, String data, ParserState state) throws Exception {
		data = data.trim();
		Matcher match = Regexes.EntitiesChosenRegex.matcher(data);
		if (match.matches()) {
			// NOTE: in 10357, "Player" is bugged, it's treating a player ID
			// as an entity ID, resulting in "Player=GameEntity"
			// For our own sanity we keep the old playerID logic from the
			// previous builds, we'll change to "player" when it's fixed.
			String rawEntity = match.group(1);
			String rawPlayer = match.group(2);
			int count = Integer.parseInt(match.group(3));
			int entity = Helper.parseEntity(rawEntity, state);
			int player = Helper.parseEntity(rawPlayer, state);

			ChosenEntities cEntities = new ChosenEntities(timestamp, entity, player, count, new ArrayList<Choice>());
			state.getCurrentGame().getData().add(cEntities);
			state.setCurrentChosenEntities(cEntities);
			return;
		}

		match = Regexes.EntitiesChosenEntitiesRegex.matcher(data);
		if (match.matches()) {
			int index = Integer.parseInt(match.group(1));
			String rawEntity = match.group(2);
			int entity = Helper.parseEntity(rawEntity, state);
			Choice choice = new Choice(entity, index);
			state.getCurrentChosenEntities().getChoices().add(choice);
			return;
		}

		log.warn("Warning: Unhandled chosen entities: " + data);
	}

}
