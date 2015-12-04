package com.hearthsim.hsreplay.parser.handlers;

import java.util.ArrayList;
import java.util.regex.Matcher;

import com.hearthsim.hsreplay.enums.ChoiceType;
import com.hearthsim.hsreplay.parser.Helper;
import com.hearthsim.hsreplay.parser.ParserState;
import com.hearthsim.hsreplay.parser.Regexes;
import com.hearthsim.hsreplay.parser.replaydata.Game;
import com.hearthsim.hsreplay.parser.replaydata.gameactions.Action;
import com.hearthsim.hsreplay.parser.replaydata.meta.Choice;
import com.hearthsim.hsreplay.parser.replaydata.meta.SendChoices;

public class SendChoicesHandler {

	public static void handle(String timestamp, String data, ParserState state) throws Exception {
		data = data.trim();
		Matcher match = Regexes.SendChoicesChoicetypeRegex.matcher(data);
		if (match.matches()) {
			String id = match.group(1);
			String rawType = match.group(2);
			int type = ChoiceType.parseEnum(rawType);

			SendChoices sendChoices = new SendChoices(timestamp, new ArrayList<>(), Integer.parseInt(id), type);
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
