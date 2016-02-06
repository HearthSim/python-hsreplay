package info.hearthsim.hsreplay.parser.handlers;

import info.hearthsim.hsreplay.enums.ChoiceType;
import info.hearthsim.hsreplay.parser.Helper;
import info.hearthsim.hsreplay.parser.ParserState;
import info.hearthsim.hsreplay.parser.Regexes;
import info.hearthsim.hsreplay.parser.replaydata.Game;
import info.hearthsim.hsreplay.parser.replaydata.gameactions.Action;
import info.hearthsim.hsreplay.parser.replaydata.meta.Choice;
import info.hearthsim.hsreplay.parser.replaydata.meta.SendChoices;

import java.util.ArrayList;
import java.util.regex.Matcher;

public class SendChoicesHandler {

	public static void handle(String timestamp, String data, ParserState state) throws Exception {
		data = data.trim();
		Matcher match = Regexes.SendChoicesChoicetypeRegex.matcher(data);
		if (match.matches()) {
			String id = match.group(1);
			String rawType = match.group(2);
			int type = ChoiceType.parseEnum(rawType);

			SendChoices sendChoices = new SendChoices(timestamp, new ArrayList<Choice>(), Integer.parseInt(id), type);
			state.setSendChoices(sendChoices);

			if (state.getNode().getType().isAssignableFrom(Game.class))
				((Game) state.getNode().getObject()).getData().add(sendChoices);
			else if (state.getNode().getType().isAssignableFrom(Action.class))
				((Action) state.getNode().getObject()).getData().add(sendChoices);
			else
				throw new Exception("Invalid node " + state.getNode().getType());
			return;
		}

		match = Regexes.SendChoicesEntitiesRegex.matcher(data);
		if (match.matches()) {
			int index = Helper.parseEntity(match.group(1), state);
			int id = Helper.parseEntity(match.group(2), state);
			Choice choice = new Choice(id, index);
			state.getSendChoices().getChoices().add(choice);
		}
	}

}
