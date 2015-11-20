#region

using System.Xml.Serialization;
using HearthstoneReplays.Parser.ReplayData.Entities;
using HearthstoneReplays.Parser.ReplayData.GameActions;
using HearthstoneReplays.Parser.ReplayData.Meta;
using HearthstoneReplays.Parser.ReplayData.Meta.Options;

#endregion

namespace HearthstoneReplays.Parser.ReplayData
{
	[XmlInclude(typeof(BaseEntity))]
	[XmlInclude(typeof(GameAction))]
	[XmlInclude(typeof(Choices))]
	[XmlInclude(typeof(SendChoices))]
	[XmlInclude(typeof(Options))]
	[XmlInclude(typeof(SendOption))]
	[XmlInclude(typeof(HideEntity))]
	[XmlInclude(typeof(ShowEntity))]
	[XmlInclude(typeof(MetaData))]
	[XmlInclude(typeof(ChosenEntities))]
	public abstract class GameData
	{
		[XmlAttribute("ts")]
		public string TimeStamp { get; set; }
	}
}