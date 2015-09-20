#region

using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.Meta
{
	[XmlRoot("Choice")]
	public class Choice : GameData
	{
		[XmlAttribute("entity")]
		public string Entity { get; set; }

		[XmlAttribute("index")]
		public string Index { get; set; }
	}
}