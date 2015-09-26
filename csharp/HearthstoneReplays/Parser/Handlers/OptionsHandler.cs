#region

using System;
using System.Collections.Generic;
using HearthstoneReplays.Hearthstone.Enums;
using HearthstoneReplays.ReplayData;
using HearthstoneReplays.ReplayData.Meta.Options;

#endregion

namespace HearthstoneReplays.Parser.Handlers
{
	public class OptionsHandler
	{
		public static void Handle(string timestamp, string data, ParserState state)
		{
			data = data.Trim();
			var match = Regexes.OptionsEntityRegex.Match(data);
			if(match.Success)
			{
				var id = match.Groups[1].Value;
				state.Options = new Options {Id = int.Parse(id), OptionList = new List<Option>()};
				if(state.Node.Type == typeof(Game))
					((Game)state.Node.Object).Data.Add(state.Options);
				else
					throw new Exception("Invalid node " + state.Node.Type + " -- " + data);
				return;
			}
			match = Regexes.OptionsOptionRegex.Match(data);
			if(match.Success)
			{
				var index = match.Groups[1].Value;
				var rawType = match.Groups[2].Value;
				var rawEntity = match.Groups[3].Value;
				var entity = Helper.ParseEntity(rawEntity, state);
			    var type = Helper.ParseEnum<OPTION_TYPE>(rawType);
				var option = new Option {Entity = entity, Index = int.Parse(index), Type = type, OptionItems = new List<OptionItem>()};
				state.Options.OptionList.Add(option);
				state.CurrentOption = option;
				state.LastOption = option;
				return;
			}
			match = Regexes.OptionsSuboptionRegex.Match(data);
			if(match.Success)
			{
				var subOptionType = match.Groups[1].Value;
				var index = match.Groups[2].Value;
				var rawEntity = match.Groups[3].Value;
				var entity = Helper.ParseEntity(rawEntity, state);

				if(subOptionType == "subOption")
				{
					var subOption = new SubOption {Entity = entity, Index = int.Parse(index), Targets = new List<Target>()};
					state.CurrentOption.OptionItems.Add(subOption);
					state.LastOption = subOption;
				}
				else if(subOptionType == "target")
				{
					var target = new Target {Entity = entity, Index = int.Parse(index)};
					var lastOption = state.LastOption as Option;
					if(lastOption != null)
					{
						lastOption.OptionItems.Add(target);
						return;
					}
					var lastSubOption = state.LastOption as SubOption;
					if(lastSubOption != null)
						lastSubOption.Targets.Add(target);
				}
				else
					throw new Exception("Unexpected suboption type: " + subOptionType);
			}
		}
	}
}