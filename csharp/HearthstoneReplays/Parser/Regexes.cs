#region

using System.Text.RegularExpressions;

#endregion

namespace HearthstoneReplays.Parser
{
	public class Regexes
	{
		public static readonly Regex PowerlogLineRegex = new Regex(@"^D ([\d:.]+) ([^(]+)\(\) - (.+)$");
		public static readonly Regex OutputlogLineRegex = new Regex(@"\[Power\] ()([^(]+)\(\) - (.+)$");
		public static readonly Regex EntityRegex = new Regex(@"\[.*\s*id=(\d+)\s*.*\]");

		public static readonly Regex ChoicesChoiceRegex =
			new Regex(@"id=(\d+) PlayerId=(\d+) ChoiceType=(\w+) CountMin=(\d+) CountMax=(\d+)$");

		public static readonly Regex ChoicesSourceRegex = new Regex(@"Source=(\[?.+\]?)$");
		public static readonly Regex ChoicesEntitiesRegex = new Regex(@"Entities\[(\d+)\]=(\[.+\])$");
		public static readonly Regex SendChoicesChoicetypeRegex = new Regex(@"id=(\d+) ChoiceType=(.+)$");
		public static readonly Regex SendChoicesEntitiesRegex = new Regex(@"m_chosenEntities\[(\d+)\]=(\[.+\])$");
		public static readonly Regex OptionsEntityRegex = new Regex(@"id=(\d+)$");
		public static readonly Regex OptionsOptionRegex = new Regex(@"option (\d+) type=(\w+) mainEntity=(.*)$");
		public static readonly Regex OptionsSuboptionRegex = new Regex(@"(subOption|target) (\d+) entity=(.*)$");

		public static readonly Regex SendOptionRegex =
			new Regex(@"selectedOption=(\d+) selectedSubOption=(-1|\d+) selectedTarget=(\d+) selectedPosition=(\d+)");

		public static readonly Regex ActionTagRegex = new Regex(@"tag=(\w+) value=(\w+)");
		public static readonly Regex ActionFullentityRegex1 = new Regex(@"FULL_ENTITY - Updating (\[.+\]) CardID=(\w+)?$");
		public static readonly Regex ActionFullentityRegex2 = new Regex(@"FULL_ENTITY - Creating ID=(\d+) CardID=(\w+)?$");
		public static readonly Regex ActionShowEntityRegex = new Regex(@"SHOW_ENTITY - Updating Entity=(\[?.+\]?) CardID=(\w+)$");
		public static readonly Regex ActionHideEntityRegex = new Regex(@"HIDE_ENTITY - Entity=(\[?.+\]?) tag=(\w+) value=(\w+)");
		public static readonly Regex ActionTagChangeRegex = new Regex(@"TAG_CHANGE Entity=(\[?.+\]?) tag=(\w+) value=(\w+)");

		public static readonly Regex ActionStartRegex =
			new Regex(@"ACTION_START Entity=(\[?.+\]?) (?:SubType|BlockType)=(\w+) Index=(-1|\d+) Target=(\[?.+\]?)$");

		public static readonly Regex ActionMetadataRegex = new Regex(@"META_DATA - Meta=(\w+) Data=(\[?.+\]?) Info=(\d+)");
		public static readonly Regex ActionCreategameRegex = new Regex(@"GameEntity EntityID=(\d+)");

		public static readonly Regex ActionCreategamePlayerRegex =
			new Regex(@"Player EntityID=(\d+) PlayerID=(\d+) GameAccountId=\[hi=(\d+) lo=(\d+)\]$");

		public static readonly Regex ActionMetaDataInfoRegex = new Regex(@"Info\[(\d+)\] = (\[?.+\]?)");
	}
}