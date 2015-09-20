#region

using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.Meta
{
	public class Info : GameData
	{
		[XmlAttribute("info")]
		public string Index { get; set; }

		[XmlAttribute("id")]
		public string Id { get; set; }
	}
}