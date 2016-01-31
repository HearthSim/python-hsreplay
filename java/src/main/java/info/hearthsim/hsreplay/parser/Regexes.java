package info.hearthsim.hsreplay.parser;

import java.text.MessageFormat;
import java.util.regex.Pattern;

public class Regexes {

	private static final String Entity = "(GameEntity|UNKNOWN HUMAN PLAYER|\\[.+\\]|\\d+|.+)";

	public static final Pattern PowerlogLineRegex = Pattern.compile("^D ([\\d:.]+) ([^(]+)\\(\\) - (.+)$");
	public static final Pattern OutputlogLineRegex = Pattern.compile("\\[Power\\] ()([^(]+)\\(\\) - (.+)$");
	public static final Pattern EntityRegex = Pattern.compile("\\[.*\\s*id=(\\d+)\\s*.*\\]");

	public static final Pattern ChoicesChoiceRegex_OLD = Pattern
			.compile("id=(\\d+) PlayerId=(\\d+) ChoiceType=(\\w+) CountMin=(\\d+) CountMax=(\\d+)$");
	public static final Pattern ChoicesChoiceRegex = Pattern.compile(MessageFormat.format(
			"id=(\\d+) Player={0} TaskList=(\\d+)? ChoiceType=(\\w+) CountMin=(\\d+) CountMax=(\\d+)$", Entity));
	public static final Pattern ChoicesSourceRegex = Pattern.compile(MessageFormat.format("Source={0}$", Entity));
	public static final Pattern ChoicesEntitiesRegex = Pattern.compile("Entities\\[(\\d+)\\]=(\\[.+\\])$");

	public static final Pattern ActionCreategameRegex = Pattern.compile("GameEntity EntityID=(\\d+)");
	public static final Pattern ActionCreategamePlayerRegex = Pattern
			.compile("Player EntityID=(\\d+) PlayerID=(\\d+) GameAccountId=\\[hi=(\\d+) lo=(\\d+)\\]$");
	public static final Pattern ActionStartRegex = Pattern.compile(MessageFormat
			.format("ACTION_START Entity={0} (?:SubType|BlockType)=(\\w+) Index=(-1|\\d+) Target={0}$", Entity));
	public static final Pattern ActionMetadataRegex = Pattern
			.compile(MessageFormat.format("META_DATA - Meta=(\\w+) Data={0} Info=(\\d+)", Entity));
	public static final Pattern ActionMetaDataInfoRegex = Pattern
			.compile(MessageFormat.format("Info\\[(\\d+)\\] = {0}", Entity));
	public static final Pattern ActionShowEntityRegex = Pattern
			.compile(MessageFormat.format("SHOW_ENTITY - Updating Entity={0} CardID=(\\w+)$", Entity));
	public static final Pattern ActionHideEntityRegex = Pattern
			.compile(MessageFormat.format("HIDE_ENTITY - Entity={0} tag=(\\w+) value=(\\w+)", Entity));
	public static final Pattern ActionFullEntityUpdatingRegex = Pattern
			.compile(MessageFormat.format("FULL_ENTITY - Updating {0} CardID=(\\w+)?$", Entity));
	public static final Pattern ActionFullEntityCreatingRegex = Pattern
			.compile("FULL_ENTITY - Creating ID=(\\d+) CardID=(\\w+)?$");
	public static final Pattern ActionTagChangeRegex = Pattern
			.compile(MessageFormat.format("TAG_CHANGE Entity={0} tag=(\\w+) value=(\\w+)", Entity));
	public static final Pattern ActionTagRegex = Pattern.compile("tag=(\\w+) value=(\\w+)");

	public static final Pattern EntitiesChosenRegex = Pattern
			.compile(MessageFormat.format("id=(\\d+) Player={0} EntitiesCount=(\\d+)$", Entity));
	public static final Pattern EntitiesChosenEntitiesRegex = Pattern
			.compile(MessageFormat.format("Entities\\[(\\d+)\\]={0}$", Entity));

	public static final Pattern OptionsEntityRegex = Pattern.compile("id=(\\d+)$");
	public static final Pattern OptionsOptionRegex = Pattern
			.compile(MessageFormat.format("option (\\d+) type=(\\w+) mainEntity={0}?$", Entity));
	public static final Pattern OptionsSuboptionRegex = Pattern
			.compile(MessageFormat.format("(subOption|target) (\\d+) entity={0}?$", Entity));

	public static final Pattern SendChoicesChoicetypeRegex = Pattern.compile("id=(\\d+) ChoiceType=(.+)$");
	public static final Pattern SendChoicesEntitiesRegex = Pattern.compile("m_chosenEntities\\[(\\d+)\\]=(\\[.+\\])$");

	public static final Pattern SendOptionRegex = Pattern
			.compile("selectedOption=(\\d+) selectedSubOption=(-1|\\d+) selectedTarget=(\\d+) selectedPosition=(\\d+)");

}
