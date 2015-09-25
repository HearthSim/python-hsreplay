#region

using System.Collections.Generic;
using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.Meta
{
	public class MetaData : GameData
	{
		[XmlAttribute("data")]
		public int Data { get; set; }

		[XmlAttribute("info")]
		public int Info { get; set; }

		[XmlAttribute("meta")]
		public int Meta { get; set; }

		[XmlElement("Info", typeof(Info))]
		public List<Info> MetaInfo { get; set; }
	}
}