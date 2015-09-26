#region

using System;
using System.Collections.Generic;
using HearthstoneReplays.Hearthstone.Enums;
using HearthstoneReplays.ReplayData.GameActions;

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
			Tags = new Dictionary<GAME_TAG, int>();
			if(tags != null)
			{
				foreach(var tag in tags)
					Tags.Add((GAME_TAG)tag.Name, tag.Value);
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
		public Dictionary<GAME_TAG, int> Tags { get; private set; }

		public bool HasTag(GAME_TAG tag)
		{
			return GetTag(tag) > 0;
		}

		public int GetTag(GAME_TAG tag)
		{
			int value;
			Tags.TryGetValue(tag, out value);
			return value;
		}

		public void SetTag(GAME_TAG tag, int value)
		{
			if(!Tags.ContainsKey(tag))
				Tags.Add(tag, value);
			else
				Tags[tag] = value;
		}

		public void SetTag(GAME_TAG tag, string value)
		{
			if(!Tags.ContainsKey(tag))
				Tags.Add(tag, ParseTagValue(tag, value));
			else
				Tags[tag] = ParseTagValue(tag, value);
		}

		public void SetTag(string tag, int value)
		{
			GAME_TAG gameTag;
			if(Enum.TryParse(tag, out gameTag))
				SetTag(gameTag, value);
		}

		public void SetTag(string tag, string value)
		{
			GAME_TAG gameTag;
			if(Enum.TryParse(tag, out gameTag))
				SetTag(gameTag, value);
		}

		private int ParseTagValue(GAME_TAG tag, string rawValue)
		{
			int value;
			if(tag == GAME_TAG.ZONE)
			{
				TAG_ZONE zone;
				Enum.TryParse(rawValue, out zone);
				value = (int)zone;
			}
			else if(tag == GAME_TAG.MULLIGAN_STATE)
			{
				TAG_MULLIGAN state;
				Enum.TryParse(rawValue, out state);
				value = (int)state;
			}
			else if(tag == GAME_TAG.PLAYSTATE)
			{
				TAG_PLAYSTATE state;
				Enum.TryParse(rawValue, out state);
				value = (int)state;
			}
			else if(tag == GAME_TAG.CARDTYPE)
			{
				TAG_CARDTYPE type;
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

		public bool IsInZone(TAG_ZONE zone)
		{
			return (TAG_ZONE)GetTag(GAME_TAG.ZONE) == zone;
		}

		public bool IsOfType(TAG_CARDTYPE type)
		{
			return (TAG_CARDTYPE)GetTag(GAME_TAG.CARDTYPE) == type;
		}
	}
}