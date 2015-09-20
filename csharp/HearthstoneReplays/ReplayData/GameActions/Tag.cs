#region

using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.GameActions
{
	public class Tag
	{
		[XmlAttribute("tag")]
		public int Name { get; set; }

		[XmlAttribute("value")]
		public int Value { get; set; }
	}
}