#region

using System;
using System.Collections.Generic;
using HearthstoneReplays.ReplayData.Meta;

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
				var type = match.Groups[2].Value;
				state.SendChoices = new SendChoices {Choices = new List<Choice>(), Entity = id, Type = type};
				if(state.Node.Type == typeof(Game))
					((Game)state.Node.Object).Data.Add(state.SendChoices);
				else
					throw new Exception("Invalid node " + state.Node.Type + " -- " + data);
				return;
			}
			match = Regexes.SendChoicesEntitiesRegex.Match(data);
			if(match.Success)
			{
				var id = match.Groups[1].Value;
				var index = match.Groups[2].Value;
				var choice = new Choice {Entity = id, Index = index};
				state.SendChoices.Choices.Add(choice);
			}
		}
	}
}