#region

using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using HearthstoneReplays.Parser.Handlers;

#endregion

namespace HearthstoneReplays.Parser
{
	public class ReplayParser
	{
		private static readonly ParserState State = new ParserState();

		public static HearthstoneReplay FromFile(string filePath)
		{
			using(var reader = new StreamReader(filePath))
				return FromTextReader(reader);
		}

		public static HearthstoneReplay FromTextReader(TextReader reader)
		{
			var lines = new List<string>();
			string line;
			while((line = reader.ReadLine()) != null)
				lines.Add(line);
			Read(lines.ToArray());
			return State.Replay;
		}

		public static HearthstoneReplay FromString(IEnumerable<string> lines)
		{
			Read(lines.ToArray());
			return State.Replay;
		}

		public static void Read(string[] lines)
		{
			State.Reset();
			State.Replay.Games = new List<Game>();
			Regex logTypeRegex = null;
			foreach(var line in lines)
			{
				Match match;
				if(logTypeRegex == null)
				{
					match = Regexes.PowerlogLineRegex.Match(line);
					if(match.Success)
						logTypeRegex = Regexes.PowerlogLineRegex;
					else
					{
						match = Regexes.OutputlogLineRegex.Match(line);
						if(match.Success)
							logTypeRegex = Regexes.OutputlogLineRegex;
					}
				}
				else
					match = logTypeRegex.Match(line);
				if(!match.Success)
					continue;
				AddData(match.Groups[1].Value, match.Groups[2].Value, match.Groups[3].Value);
			}
		}

		private static void AddData(string timestamp, string method, string data)
		{
			switch(method)
			{
				case "GameState.DebugPrintPower":
					DataHandler.Handle(timestamp, data, State);
					break;
				case "GameState.SendChoices":
					SendChoicesHandler.Handle(timestamp, data, State);
					break;
				case "GameState.DebugPrintChoices":
					ChoicesHandler.Handle(timestamp, data, State);
					break;
				case "GameState.DebugPrintOptions":
					OptionsHandler.Handle(timestamp, data, State);
					break;
				case "GameState.SendOption":
					SendOptionHandler.Handle(timestamp, data, State);
					break;
			}
		}
	}
}