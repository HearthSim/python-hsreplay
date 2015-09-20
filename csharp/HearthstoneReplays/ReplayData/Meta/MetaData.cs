#region

using System.Collections.Generic;
using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.Meta
{
	public class MetaData : GameData
	{
		[XmlAttribute("data")]
		public string Data { get; set; }

		[XmlAttribute("info")]
		public string Info { get; set; }

		[XmlAttribute("meta")]
		public int Meta { get; set; }

		[XmlElement("Info", typeof(Info))]
		public List<Info> MetaInfo { get; set; }
	}
}