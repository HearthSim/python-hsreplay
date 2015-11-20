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
	public class SendChoicesHandler
	{
		public static void Handle(string timestamp, string data, ParserState state)
		{
			data = data.Trim();
			var match = Regexes.SendChoicesChoicetypeRegex.Match(data);
			if(match.Success)
			{
				var id = match.Groups[1].Value;
				var rawType = match.Groups[2].Value;
			    var type = Helper.ParseEnum<ChoiceType>(rawType);
				state.SendChoices = new SendChoices {Choices = new List<Choice>(), Entity = int.Parse(id), Type = type, TimeStamp = timestamp};
				if(state.Node.Type == typeof(Game))
					((Game)state.Node.Object).Data.Add(state.SendChoices);
				else if(state.Node.Type == typeof(Action))
					((Action)state.Node.Object).Data.Add(state.SendChoices);
				else
					throw new Exception("Invalid node " + state.Node.Type + " -- " + data);
				return;
			}
			match = Regexes.SendChoicesEntitiesRegex.Match(data);
			if(match.Success)
			{
				var index = Helper.ParseEntity(match.Groups[1].Value, state);
				var id = Helper.ParseEntity(match.Groups[2].Value, state);
				var choice = new Choice {Entity = id, Index = index};
				state.SendChoices.Choices.Add(choice);
			}
		}
	}
}