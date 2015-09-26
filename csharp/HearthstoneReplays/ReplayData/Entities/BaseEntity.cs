#region

using System.Collections.Generic;
using System.Linq;
using System.Xml.Serialization;
using HearthstoneReplays.ReplayData.GameActions;

#endregion

namespace HearthstoneReplays.ReplayData.Entities
{
	[XmlInclude(typeof(GameEntity))]
	[XmlInclude(typeof(PlayerEntity))]
	[XmlInclude(typeof(FullEntity))]
	public abstract class BaseEntity : GameData
	{
		[XmlAttribute("id")]
		public int Id { get; set; }

		[XmlElement("Tag", typeof(Tag))]
		public List<Tag> Tags { get; set; }

		public override bool Equals(object obj)
		{
			var other = obj as BaseEntity;
			if(other == null)
				return false;
			return Id == other.Id && Tags.All(tag => other.Tags.Any(t1 => t1.Name == tag.Name && t1.Value == tag.Value));
		}
	}
}