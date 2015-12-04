package com.hearthsim.hsreplay.parser.handlers;

import java.util.regex.Matcher;

import com.hearthsim.hsreplay.parser.ParserState;
import com.hearthsim.hsreplay.parser.Regexes;
import com.hearthsim.hsreplay.parser.replaydata.Game;
import com.hearthsim.hsreplay.parser.replaydata.meta.options.SendOption;

public class SendOptionHandler {

	public static void handle(String timestamp, String data, ParserState state) throws Exception {
		data = data.trim();
		Matcher match = Regexes.SendOptionRegex.matcher(data);
		if (match.matches()) {
			String option = match.group(1);
			String suboption = match.group(2);
			String target = match.group(3);
			String position = match.group(4);

			SendOption sendOption = SendOption.builder().optionIndex(Integer.parseInt(option))
					.position(Integer.parseInt(position)).subOption(Integer.parseInt(suboption))
					.target(Integer.parseInt(target)).build();

			if (state.getNode().getType().isAssignableFrom(Game.class))
				((Game) state.getNode().getObject()).getData().add(sendOption);
			else
				throw new Exception("Invalid node " + state.getNode().getType());
		}
	}
}
