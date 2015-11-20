#region

using System.Collections.Generic;
using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.Parser.ReplayData.GameActions
{
	public class ShowEntity : GameData

	{
		[XmlAttribute("cardID")]
		public string CardId { get; set; }

		[XmlAttribute("entity")]
		public int Entity { get; set; }

		[XmlElement("Tag", typeof(Tag))]
		public List<Tag> Tags { get; set; }
	}
}