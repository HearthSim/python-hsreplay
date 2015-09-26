#region

using System.Xml.Serialization;
using HearthstoneReplays.ReplayData.Entities;
using HearthstoneReplays.ReplayData.GameActions;
using HearthstoneReplays.ReplayData.Meta;
using HearthstoneReplays.ReplayData.Meta.Options;

#endregion

namespace HearthstoneReplays.ReplayData
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