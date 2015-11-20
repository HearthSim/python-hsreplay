#region

using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.Parser.ReplayData.Meta.Options
{
	public class SendOption : GameData
	{
		[XmlAttribute("option")]
		public int OptionIndex { get; set; }

		[XmlAttribute("position")]
		public int Position { get; set; }

		[XmlAttribute("suboption")]
		public int SubOption { get; set; }

		[XmlAttribute("target")]
		public int Target { get; set; }
	}
}