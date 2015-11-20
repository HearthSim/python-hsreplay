using System;
using System.Collections.Generic;
using HearthstoneReplays.Parser.ReplayData.GameActions;
using HearthstoneReplays.Parser.ReplayData.Meta;

namespace HearthstoneReplays.Parser.Handlers
{
	public class EntityChosenHandler
	{
		public static void Handle(string timestamp, string data, ParserState state)
		{
			data = data.Trim();
			var match = Regexes.EntitiesChosenRegex.Match(data);
			if(match.Success)
			{
				/*NOTE: in 10357, "Player" is bugged, it's treating a player ID
				as an entity ID, resulting in "Player=GameEntity"
				For our own sanity we keep the old playerID logic from the
				previous builds, we'll change to "player" when it's fixed.*/
				var rawEntity = match.Groups[1].Value;
				var rawPlayer = match.Groups[2].Value;
				var count = int.Parse(match.Groups[3].Value);
				var entity = Helper.ParseEntity(rawEntity, state);
				var player = Helper.ParseEntity(rawPlayer, state);
				var cEntities = new ChosenEntities {Entity = entity, PlayerId = player, Count = count, Choices = new List<Choice>(), TimeStamp = timestamp};
				state.CurrentGame.Data.Add(cEntities);
				state.CurrentChosenEntites = cEntities;
				return;
			}
			match = Regexes.EntitiesChosenEntitiesRegex.Match(data);
			if(match.Success)
			{
				var index = int.Parse(match.Groups[1].Value);
				var rawEntity = match.Groups[2].Value;
				var entity = Helper.ParseEntity(rawEntity, state);
				var choice = new Choice {Entity = entity, Index = index};
				state.CurrentChosenEntites.Choices.Add(choice);
				return;
			}
			Console.WriteLine("Warning: Unhandled chosen entities: " + data);
		}
	}
}