#region

using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.Entities
{
	[XmlRoot("FullEntity")]
	public class FullEntity : BaseEntity
	{
		[XmlAttribute("cardID")]
		public string CardId { get; set; }

		public bool ShouldSerializeCardId()
		{
			return !string.IsNullOrEmpty(CardId);
		}
	}
}