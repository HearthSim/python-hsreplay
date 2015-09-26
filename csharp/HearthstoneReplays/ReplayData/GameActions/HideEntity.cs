#region

using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.GameActions
{
	public class HideEntity : GameData
	{
		[XmlAttribute("entity")]
		public int Entity { get; set; }

		[XmlAttribute("tag")]
		public int TagName { get; set; }

		[XmlAttribute("value")]
		public int TagValue { get; set; }
	}
}