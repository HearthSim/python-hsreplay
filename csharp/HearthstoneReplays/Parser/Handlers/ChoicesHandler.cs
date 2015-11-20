#region

using System;
using System.Collections.Generic;
using HearthDb.Enums;
using HearthstoneReplays.Parser.ReplayData;
using HearthstoneReplays.Parser.ReplayData.Meta;
using Action = HearthstoneReplays.Parser.ReplayData.GameActions.Action;

#endregion

namespace HearthstoneReplays.Parser.Handlers
{
	public class ChoicesHandler
	{
		public static void Handle(string timestamp, string data, ParserState state)
		{
			data = data.Trim();
			var match = Regexes.ChoicesChoiceRegex_OLD.Match(data);
			if(match.Success)
			{
				var rawEntity = match.Groups[1].Value;
				var playerId = match.Groups[2].Value;
				var rawType = match.Groups[3].Value;
				var min = match.Groups[4].Value;
				var max = match.Groups[5].Value;
				var entity = Helper.ParseEntity(rawEntity, state);
				var type = Helper.ParseEnum<ChoiceType>(rawType);
				state.Choices = new Choices
				{
					ChoiceList = new List<Choice>(),
					Entity = entity,
					Max = int.Parse(max),
					Min = int.Parse(min),
					PlayerId = int.Parse(playerId),
					Type = type
				};
				if(state.Node.Type == typeof(Game))
					((Game)state.Node.Object).Data.Add(state.Choices);
				else if(state.Node.Type == typeof(Action))
					((Action)state.Node.Object).Data.Add(state.Choices);
				else
					throw new Exception("Invalid node " + state.Node.Type + " -- " + data);
				return;
			}

			match = Regexes.ChoicesChoiceRegex.Match(data);
			if(match.Success)
			{
				/*NOTE: in 10357, "Player" is bugged, it's treating a player ID
				as an entity ID, resulting in "Player=GameEntity"
				For our own sanity we keep the old playerID logic from the
				previous builds, we'll change to "player" when it's fixed.*/
				var rawEntity = match.Groups[1].Value;
				var rawPlayer = match.Groups[2].Value;
				var taskList = match.Groups[3].Value;
				var rawType = match.Groups[4].Value;
				var min = match.Groups[5].Value;
				var max = match.Groups[6].Value;
				var entity = Helper.ParseEntity(rawEntity, state);
				var player = Helper.ParseEntity(rawPlayer, state);
				var type = Helper.ParseEnum<ChoiceType>(rawType);
				state.Choices = new Choices
				{
					ChoiceList = new List<Choice>(),
					Entity = entity,
					Max = int.Parse(max),
					Min = int.Parse(min),
					PlayerId = player,
					TaskList = int.Parse(taskList),
					Type = type
				};
				if(state.Node.Type == typeof(Game))
					((Game)state.Node.Object).Data.Add(state.Choices);
				else if(state.Node.Type == typeof(Action))
					((Action)state.Node.Object).Data.Add(state.Choices);
				else
					throw new Exception("Invalid node " + state.Node.Type + " -- " + data);
				return;
			}

			match = Regexes.ChoicesSourceRegex.Match(data);
			if(match.Success)
			{
				var rawEntity = match.Groups[1].Value;
				var entity = Helper.ParseEntity(rawEntity, state);
				state.Choices.Source = entity;
				return;
			}

			match = Regexes.ChoicesEntitiesRegex.Match(data);
			if(match.Success)
			{
				var index = match.Groups[1].Value;
				var rawEntity = match.Groups[2].Value;
				var entity = Helper.ParseEntity(rawEntity, state);
				var choice = new Choice {Entity = entity, Index = int.Parse(index)};
				state.Choices.ChoiceList.Add(choice);
			}
		}
	}
}