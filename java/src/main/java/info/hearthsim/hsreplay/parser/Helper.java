package info.hearthsim.hsreplay.parser;

import info.hearthsim.hsreplay.enums.CardClass;
import info.hearthsim.hsreplay.enums.CardType;
import info.hearthsim.hsreplay.enums.Faction;
import info.hearthsim.hsreplay.enums.GameTag;
import info.hearthsim.hsreplay.enums.Mulligan;
import info.hearthsim.hsreplay.enums.PlayState;
import info.hearthsim.hsreplay.enums.Rarity;
import info.hearthsim.hsreplay.enums.State;
import info.hearthsim.hsreplay.enums.Step;
import info.hearthsim.hsreplay.enums.Zone;
import info.hearthsim.hsreplay.parser.replaydata.GameData;
import info.hearthsim.hsreplay.parser.replaydata.entities.PlayerEntity;
import info.hearthsim.hsreplay.parser.replaydata.gameactions.Tag;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.regex.Matcher;

import org.apache.commons.lang.StringUtils;

public class Helper {

	private static final Map<Integer, Class> tagTypes = buildTags();

	public static int parseEntity(String data, ParserState state) throws Exception {
		if (!StringUtils.isNotEmpty(data)) return 0;

		Matcher match = Regexes.EntityRegex.matcher(data);
		if (match.matches()) return Integer.parseInt(match.group(1));
		if (data.equals("GameEntity")) return 1;
		try {
			int numeric = Integer.parseInt(data);
			return numeric;
		}
		catch (Exception e) {
		}
		return getPlayerIdFromName(data, state);
	}

	private static Map<Integer, Class> buildTags() {
		Map<Integer, Class> tags = new HashMap<>();
		tags.put(GameTag.CARDTYPE.getIntValue(), CardType.class);
		tags.put(GameTag.CLASS.getIntValue(), CardClass.class);
		tags.put(GameTag.FACTION.getIntValue(), Faction.class);
		tags.put(GameTag.PLAYSTATE.getIntValue(), PlayState.class);
		tags.put(GameTag.RARITY.getIntValue(), Rarity.class);
		tags.put(GameTag.MULLIGAN_STATE.getIntValue(), Mulligan.class);
		tags.put(GameTag.NEXT_STEP.getIntValue(), Step.class);
		tags.put(GameTag.STATE.getIntValue(), State.class);
		tags.put(GameTag.STEP.getIntValue(), Step.class);
		tags.put(GameTag.ZONE.getIntValue(), Zone.class);
		return tags;
	}

	private static int getPlayerIdFromName(String data, ParserState state) throws Exception {
		Optional<GameData> optFirstPlayer = state.getCurrentGame().getData().stream()
				.filter(x -> x instanceof PlayerEntity && ((PlayerEntity) x).getId() == state.getFirstPlayerId())
				.findFirst();

		if (!optFirstPlayer.isPresent()) throw new Exception("Could not find first player " + data + " " + state);
		PlayerEntity firstPlayer = (PlayerEntity) optFirstPlayer.get();

		Optional<GameData> optSecondPlayer = state.getCurrentGame().getData().stream()
				.filter(x -> x instanceof PlayerEntity && ((PlayerEntity) x).getId() != state.getFirstPlayerId())
				.findFirst();

		if (!optSecondPlayer.isPresent()) throw new Exception("Could not find second player " + data + " " + state);
		PlayerEntity secondPlayer = (PlayerEntity) optSecondPlayer.get();

		if (data.equals(firstPlayer.getName())) return firstPlayer.getId();
		if (data.equals(secondPlayer.getName())) return secondPlayer.getId();

		if (StringUtils.isEmpty(firstPlayer.getName())) {
			firstPlayer.setName(data);
			return firstPlayer.getId();
		}
		if (StringUtils.isEmpty(secondPlayer.getName())) {
			secondPlayer.setName(data);
			return secondPlayer.getId();
		}

		if ("UNKNOWN HUMAN PLAYER".equals(firstPlayer.getName()) || "The Innkeeper".equals(firstPlayer.getName())) {
			firstPlayer.setName(data);
			return firstPlayer.getId();
		}
		if ("UNKNOWN HUMAN PLAYER".equals(secondPlayer.getName()) || "The Innkeeper".equals(secondPlayer.getName())) {
			secondPlayer.setName(data);
			return secondPlayer.getId();
		}

		throw new Exception("Could not get id from player name:" + data);
	}

	@SuppressWarnings("unchecked")
	public static Tag parseTag(String tagName, String value) throws Exception {
		Class tagType = null;
		Tag tag = new Tag();

		tag.setName(GameTag.parseEnum(tagName));

		if (tagTypes.containsKey(tag.getName())) {
			tagType = tagTypes.get(tag.getName());
			// TODO: not clean. That's what you get when you translate directly
			// from C# to Java...
			tag.setValue((Integer) tagType.getMethod("parseEnum", String.class).invoke(null, value));
		}
		else {
			try {
				int tagValue = Integer.parseInt(value);
				tag.setValue(tagValue);
			}
			catch (Exception e) {
				throw new Exception(String.format("Unhandled tag value: {0}={1}", tagName, value));
			}
		}
		return tag;
	}

}
