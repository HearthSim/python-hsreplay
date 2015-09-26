#region

using System.Collections.Generic;
using System.Xml.Serialization;
using HearthstoneReplays.ReplayData.Entities;
using HearthstoneReplays.ReplayData.GameActions;
using HearthstoneReplays.ReplayData.Meta;
using HearthstoneReplays.ReplayData.Meta.Options;

#endregion

namespace HearthstoneReplays.ReplayData
{
	public class Game
	{
		[XmlAttribute("timestamp")]
		public string TimeStamp { get; set; }

		[XmlElement("Action", typeof(Action))]
		[XmlElement("Choices", typeof(Choices))]
		[XmlElement("FullEntity", typeof(FullEntity))]
		[XmlElement("GameEntity", typeof(GameEntity))]
		[XmlElement("ShowEntity", typeof(ShowEntity))]
		[XmlElement("HideEntity", typeof(HideEntity))]
		[XmlElement("Options", typeof(Options))]
		[XmlElement("Player", typeof(PlayerEntity))]
		[XmlElement("SendChoices", typeof(SendChoices))]
		[XmlElement("SendOption", typeof(SendOption))]
		[XmlElement("TagChange", typeof(TagChange))]
		[XmlElement("MetaData", typeof(MetaData))]
		public List<GameData> Data { get; set; }
	}
}