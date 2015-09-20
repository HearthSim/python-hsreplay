#region

using System.Collections.Generic;
using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.Meta.Options
{
	public class Options : GameData
	{
		[XmlAttribute("id")]
		public string Id { get; set; }

		public List<Option> OptionList { get; set; }
	}
}