#region

using System.Collections.Generic;
using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.Meta.Options
{
	[XmlRoot("Option")]
	public class Option : GameData
	{
		[XmlAttribute("index")]
		public int Index { get; set; }

		[XmlAttribute("type")]
		public string Type { get; set; }

		[XmlAttribute("entity")]
		public string Entity { get; set; }

		[XmlElement("SubOption", typeof(SubOption))]
		[XmlElement("Target", typeof(Target))]
		public List<OptionItem> OptionItems { get; set; }
	}
}