#region

using System;
using System.Collections.Generic;
using System.Linq;
using HearthDb.Enums;
using HearthstoneReplays.Parser.ReplayData.Entities;
using HearthstoneReplays.Parser.ReplayData.GameActions;
using Type = System.Type;

#endregion

namespace HearthstoneReplays.Parser
{
	public class Helper
	{
		private static readonly Dictionary<GameTag, Type> TagTypes = new Dictionary<GameTag, Type>
		{
			{GameTag.CARDTYPE, typeof(CardType)},
			{GameTag.CLASS, typeof(CardClass)},
			{GameTag.FACTION, typeof(Faction)},
			{GameTag.PLAYSTATE, typeof(PlayState)},
			{GameTag.RARITY, typeof(Rarity)},
			{GameTag.MULLIGAN_STATE, typeof(Mulligan)},
			{GameTag.NEXT_STEP, typeof(Step)},
			{GameTag.STATE, typeof(State)},
			{GameTag.STEP, typeof(Step)},
			{GameTag.ZONE, typeof(Zone)}
		};

		public static int ParseEntity(string data, ParserState state)
		{
		    if (string.IsNullOrEmpty(data))
		        return 0;
            var match = Regexes.EntityRegex.Match(data);
			if(match.Success)
				return int.Parse(match.Groups[1].Value);
			if(data == "GameEntity")
				return 1;
			int numeric;
			if(int.TryParse(data, out numeric))
				return numeric;
			return GetPlayerIdFromName(data, state);
		}

		public static int GetPlayerIdFromName(string data, ParserState state)
		{
			var firstPlayer =
				(PlayerEntity)state.CurrentGame.Data.FirstOrDefault(x => (x is PlayerEntity) && ((PlayerEntity)x).Id == state.FirstPlayerId);
			if(firstPlayer == null)
				throw new Exception("Could not find first player");

            var secondPlayer =
                (PlayerEntity)state.CurrentGame.Data.FirstOrDefault(x => (x is PlayerEntity) && ((PlayerEntity)x).Id != state.FirstPlayerId);
            if(secondPlayer == null)
                throw new Exception("Could not find second player");

            if(firstPlayer.Name == data)
                return firstPlayer.Id;
            if(secondPlayer.Name == data)
                return secondPlayer.Id;

		    if (string.IsNullOrEmpty(firstPlayer.Name))
		    {
		        firstPlayer.Name = data;
                return firstPlayer.Id;
            }
		    if (string.IsNullOrEmpty(secondPlayer.Name))
		    {
		        secondPlayer.Name = data;
                return secondPlayer.Id;
            }

			if(firstPlayer.Name == "UNKNOWN HUMAN PLAYER" || firstPlayer.Name == "The Innkeeper")
			{
				firstPlayer.Name = data;
				return firstPlayer.Id;
			}
			if(secondPlayer.Name == "UNKNOWN HUMAN PLAYER" || secondPlayer.Name == "The Innkeeper")
			{
				secondPlayer.Name = data;
				return secondPlayer.Id;
			}


			throw new Exception("Could not get id from player name:" + data);
		}

		public static Tag ParseTag(string tagName, string value)
		{
			Type tagType;
			int tagValue;

			var tag = new Tag();
			tag.Name = ParseEnum<GameTag>(tagName);

			if(TagTypes.TryGetValue((GameTag)tag.Name, out tagType))
				tag.Value = ParseEnum(tagType, value);
			else if(int.TryParse(value, out tagValue))
				tag.Value = tagValue;
			else
				throw new Exception(string.Format("Unhandled tag value: {0}={1}", tagName, value));
			return tag;
		}

		public static int ParseEnum(Type type, string tag)
		{
			int value;
			if(int.TryParse(tag, out value))
				return value;
			var index = type.GetEnumNames().ToList().IndexOf(tag);
			if(index > -1)
				return (int)type.GetEnumValues().GetValue(index);
			throw new Exception("Enum not found: " + tag);
		}

		public static int ParseEnum<T>(string tag)
		{
			return ParseEnum(typeof(T), tag);
		}
	}
}