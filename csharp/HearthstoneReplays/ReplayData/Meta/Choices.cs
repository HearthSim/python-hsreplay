#region

using System.Collections.Generic;
using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.Meta
{
	[XmlRoot("Choices")]
	public class Choices : GameData
	{
		[XmlAttribute("entity")]
		public string Entity { get; set; }

		[XmlAttribute("max")]
		public int Max { get; set; }

		[XmlAttribute("min")]
		public int Min { get; set; }

		[XmlAttribute("playerID")]
		public int PlayerId { get; set; }

		[XmlAttribute("source")]
		public int Source { get; set; }

		[XmlAttribute("type")]
		public string Type { get; set; }

		[XmlElement("Choice", typeof(Choice))]
		public List<Choice> ChoiceList { get; set; }
	}
}