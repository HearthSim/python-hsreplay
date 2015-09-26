#region

using System.Xml.Serialization;

#endregion

namespace HearthstoneReplays.ReplayData.GameActions
{
	public class TagChange : GameAction
	{
		[XmlAttribute("tag")]
		public int Name { get; set; }

		[XmlAttribute("value")]
		public int Value { get; set; }

		public override bool Equals(object obj)
		{
			var other = obj as TagChange;
			if(other == null)
				return false;
			return other.Name == Name && other.Value == Value;
		}
	}
}