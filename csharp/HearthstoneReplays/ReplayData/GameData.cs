#region

using System.Xml.Serialization;
using HearthstoneReplays.Entities;
using HearthstoneReplays.GameActions;
using HearthstoneReplays.ReplayData.Meta;
using HearthstoneReplays.ReplayData.Meta.Options;

#endregion

namespace HearthstoneReplays
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
	public abstract class GameData
	{
		[XmlAttribute("timestamp")]
		public string TimeStamp { get; set; }
	}
}