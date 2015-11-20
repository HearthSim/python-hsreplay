#region

using System.Collections.Generic;
using System.Xml.Serialization;
using HearthstoneReplays.Parser.ReplayData.Entities;
using HearthstoneReplays.Parser.ReplayData.Meta;
using HearthstoneReplays.Parser.ReplayData.Meta.Options;

#endregion

namespace HearthstoneReplays.Parser.ReplayData.GameActions
{
	public class Action : GameAction
	{
		[XmlAttribute("index")]
		public int Index { get; set; }

		[XmlAttribute("target")]
		public int Target { get; set; }

		[XmlAttribute("type")]
		public int Type { get; set; }

		[XmlElement("Action", typeof(Action))]
		[XmlElement("Choices", typeof(Choices))]
		[XmlElement("FullEntity", typeof(FullEntity))]
		[XmlElement("ShowEntity", typeof(ShowEntity))]
		[XmlElement("HideEntity", typeof(HideEntity))]
		[XmlElement("GameEntity", typeof(GameEntity))]
		[XmlElement("Options", typeof(Options))]
		[XmlElement("Player", typeof(PlayerEntity))]
		[XmlElement("SendChoices", typeof(SendChoices))]
		[XmlElement("SendOption", typeof(SendOption))]
		[XmlElement("TagChange", typeof(TagChange))]
		[XmlElement("MetaData", typeof(MetaData))]
		[XmlElement("ChosenEntities", typeof(ChosenEntities))]
		public List<GameData> Data { get; set; }
	}
}