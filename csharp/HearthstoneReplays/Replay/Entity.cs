#region

using System;
using System.Collections.Generic;
using HearthDb.Enums;
using HearthstoneReplays.Parser.ReplayData.GameActions;

#endregion

namespace HearthstoneReplays.Replay
{
	[Serializable]
	public class Entity
	{
		public Entity(int id, string cardId = null, List<Tag> tags = null)
		{
			Id = id;
			CardId = cardId;
			Tags = new Dictionary<GameTag, int>();
			if(tags != null)
			{
				foreach(var tag in tags)
					Tags.Add((GameTag)tag.Name, tag.Value);
			}
		}

		public Entity(int id, List<Tag> tags, int playerId) : this(id, null, tags)
		{
			PlayerId = playerId;
		}

		public int Id { get; private set; }
		public string CardId { get; private set; }
		public int? PlayerId { get; private set; }
		public string Name { get; set; }
		public Dictionary<GameTag, int> Tags { get; private set; }

		public bool HasTag(GameTag tag)
		{
			return GetTag(tag) > 0;
		}

		public int GetTag(GameTag tag)
		{
			int value;
			Tags.TryGetValue(tag, out value);
			return value;
		}

		public void SetTag(GameTag tag, int value)
		{
			if(!Tags.ContainsKey(tag))
				Tags.Add(tag, value);
			else
				Tags[tag] = value;
		}

		public void SetTag(GameTag tag, string value)
		{
			if(!Tags.ContainsKey(tag))
				Tags.Add(tag, ParseTagValue(tag, value));
			else
				Tags[tag] = ParseTagValue(tag, value);
		}

		public void SetTag(string tag, int value)
		{
			GameTag gameTag;
			if(Enum.TryParse(tag, out gameTag))
				SetTag(gameTag, value);
		}

		public void SetTag(string tag, string value)
		{
			GameTag gameTag;
			if(Enum.TryParse(tag, out gameTag))
				SetTag(gameTag, value);
		}

		private int ParseTagValue(GameTag tag, string rawValue)
		{
			int value;
			if(tag == GameTag.ZONE)
			{
				Zone zone;
				Enum.TryParse(rawValue, out zone);
				value = (int)zone;
			}
			else if(tag == GameTag.MULLIGAN_STATE)
			{
				Mulligan state;
				Enum.TryParse(rawValue, out state);
				value = (int)state;
			}
			else if(tag == GameTag.PLAYSTATE)
			{
				PlayState state;
				Enum.TryParse(rawValue, out state);
				value = (int)state;
			}
			else if(tag == GameTag.CARDTYPE)
			{
				CardType type;
				Enum.TryParse(rawValue, out type);
				value = (int)type;
			}
			else
				int.TryParse(rawValue, out value);
			return value;
		}

		public void SetCardId(string cardId)
		{
			if(string.IsNullOrEmpty(CardId))
				CardId = cardId;
		}

		public bool IsInZone(Zone zone)
		{
			return (Zone)GetTag(GameTag.ZONE) == zone;
		}

		public bool IsOfType(CardType type)
		{
			return (CardType)GetTag(GameTag.CARDTYPE) == type;
		}
	}
}