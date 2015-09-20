#region

using System;
using System.Collections.Generic;
using System.Linq;
using HearthstoneReplays.Entities;
using HearthstoneReplays.GameActions;
using HearthstoneReplays.Hearthstone.Enums;

#endregion

namespace HearthstoneReplays.Parser
{
	public class Helper
	{
		private static readonly Dictionary<GAME_TAG, Type> TagTypes = new Dictionary<GAME_TAG, Type>
		{
			{GAME_TAG.CARDTYPE, typeof(TAG_CARDTYPE)},
			{GAME_TAG.CLASS, typeof(TAG_CLASS)},
			{GAME_TAG.FACTION, typeof(TAG_FACTION)},
			{GAME_TAG.PLAYSTATE, typeof(TAG_PLAYSTATE)},
			{GAME_TAG.RARITY, typeof(TAG_RARITY)},
			{GAME_TAG.MULLIGAN_STATE, typeof(TAG_MULLIGAN)},
			{GAME_TAG.NEXT_STEP, typeof(TAG_STEP)},
			{GAME_TAG.STATE, typeof(TAG_STATE)},
			{GAME_TAG.STEP, typeof(TAG_STEP)},
			{GAME_TAG.ZONE, typeof(TAG_ZONE)}
		};

		public static string ParseEntity(string data, ParserState state)
		{
			if(string.IsNullOrEmpty(data))
				return null;
			var match = Regexes.EntityRegex.Match(data);
			if(match.Success)
				return match.Groups[1].Value;
			if(data == "0")
				return null;
			if(data == "GameEntity")
				return "1";
			int numeric;
			if(int.TryParse(data, out numeric))
				return data;
			return GetPlayerIdFromName(data, state);
		}

		public static string GetPlayerIdFromName(string data, ParserState state)
		{
			var firstPlayer =
				(PlayerEntity)state.CurrentGame.Data.FirstOrDefault(x => (x is PlayerEntity) && ((PlayerEntity)x).Id == state.FirstPlayerId);
			if(firstPlayer == null)
				throw new Exception("Could not find first player");
			if(string.IsNullOrEmpty(firstPlayer.Name))
				firstPlayer.Name = data;
			if(firstPlayer.Name == data)
				return firstPlayer.Id.ToString();

			var secondPlayer =
				(PlayerEntity)state.CurrentGame.Data.FirstOrDefault(x => (x is PlayerEntity) && ((PlayerEntity)x).Id != state.FirstPlayerId);
			if(secondPlayer == null)
				throw new Exception("Could not find second player");

			if(string.IsNullOrEmpty(secondPlayer.Name))
				secondPlayer.Name = data;
			if(secondPlayer.Name == data)
				return secondPlayer.Id.ToString();

			if(firstPlayer.Name == "UNKNOWN HUMAN PLAYER")
			{
				firstPlayer.Name = data;
				return firstPlayer.Id.ToString();
			}
			if(secondPlayer.Name == "UNKNOWN HUMAN PLAYER")
			{
				secondPlayer.Name = data;
				return secondPlayer.Id.ToString();
			}


			throw new Exception("Could not get id from player name:" + data);
		}

		public static Tag ParseTag(string tagName, string value)
		{
			Type tagType;
			int tagValue;

			var tag = new Tag();
			tag.Name = ParseEnum<GAME_TAG>(tagName);

			if(TagTypes.TryGetValue((GAME_TAG)tag.Name, out tagType))
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