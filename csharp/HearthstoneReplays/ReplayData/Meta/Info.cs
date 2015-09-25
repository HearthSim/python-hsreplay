#region

using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.Meta
{
	public class Info : GameData
	{
		[XmlAttribute("info")]
		public int Index { get; set; }

		[XmlAttribute("id")]
		public int Id { get; set; }
	}
}