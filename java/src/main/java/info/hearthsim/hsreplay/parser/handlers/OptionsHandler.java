package info.hearthsim.hsreplay.parser.handlers;

import info.hearthsim.hsreplay.enums.OptionType;
import info.hearthsim.hsreplay.parser.Helper;
import info.hearthsim.hsreplay.parser.ParserState;
import info.hearthsim.hsreplay.parser.Regexes;
import info.hearthsim.hsreplay.parser.replaydata.Game;
import info.hearthsim.hsreplay.parser.replaydata.meta.options.Option;
import info.hearthsim.hsreplay.parser.replaydata.meta.options.Options;
import info.hearthsim.hsreplay.parser.replaydata.meta.options.SubOption;
import info.hearthsim.hsreplay.parser.replaydata.meta.options.Target;

import java.util.ArrayList;
import java.util.regex.Matcher;

public class OptionsHandler {

	public static void handle(String timestamp, String data, ParserState state) throws Exception {
		data = data.trim();
		Matcher match = Regexes.OptionsEntityRegex.matcher(data);
		if (match.matches()) {
			String id = match.group(1);
			Options options = new Options(timestamp, Integer.parseInt(id), new ArrayList<>());
			state.setOptions(options);
			state.updateCurrentNode(Game.class);

			if (state.getNode().getType().isAssignableFrom(Game.class))
				((Game) state.getNode().getObject()).getData().add(options);
			else
				throw new Exception("Invalid node " + state.getNode().getType());

			return;
		}

		match = Regexes.OptionsOptionRegex.matcher(data);
		if (match.matches()) {
			String index = match.group(1);
			String rawType = match.group(2);
			String rawEntity = match.group(3);

			int entity = Helper.parseEntity(rawEntity, state);
			int type = OptionType.parseEnum(rawType);

			Option option = new Option(Integer.parseInt(index), type, entity, new ArrayList<>());
			state.getOptions().getOptionList().add(option);
			state.setCurrentOption(option);
			state.setLastOption(option);
			return;
		}

		match = Regexes.OptionsSuboptionRegex.matcher(data);
		if (match.matches()) {
			String subOptionType = match.group(1);
			String index = match.group(2);
			String rawEntity = match.group(3);
			int entity = Helper.parseEntity(rawEntity, state);

			if ("subOption".equals(subOptionType)) {
				SubOption subOption = new SubOption(entity, Integer.parseInt(index), new ArrayList<>());
				state.getCurrentOption().getOptionsItems().add(subOption);
				state.setLastOption(subOption);
			}
			else if ("target".equals(subOptionType)) {
				Target target = new Target(entity, Integer.parseInt(index));
				Option lastOption = state.getLastOption() instanceof Option ? (Option) state.getLastOption() : null;
				if (lastOption != null) {
					lastOption.getOptionsItems().add(target);
					return;
				}
				SubOption lastSubOption = state.getLastOption() instanceof SubOption ? (SubOption) state
						.getLastOption() : null;
				if (lastSubOption != null) {
					lastSubOption.getTargets().add(target);
				}
			}
			else
				throw new Exception("Unexpected suboption type: " + subOptionType);
		}

	}

}
