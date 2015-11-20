#region

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;
using HearthDb.Enums;
using HearthstoneReplays.Parser.Handlers;
using HearthstoneReplays.Parser.ReplayData;

#endregion

namespace HearthstoneReplays.Parser
{
	public class ReplayParser
	{
		public const string Version = "1.0";
		public const int HearthstoneBuild = 10833;
		private static readonly ParserState State = new ParserState();

		public static HearthstoneReplay FromFile(string filePath, int hsBuild = HearthstoneBuild, params GameType[] gameTypes)
		{
			using(var reader = new StreamReader(filePath))
				return FromTextReader(reader);
		}

		public static HearthstoneReplay FromTextReader(TextReader reader, int hsBuild = HearthstoneBuild, params GameType[] gameTypes)
		{
			var lines = new List<string>();
			string line;
			while((line = reader.ReadLine()) != null)
				lines.Add(line);
			return FromString(lines);
		}

		public static HearthstoneReplay FromString(IEnumerable<string> lines, int hsBuild = HearthstoneBuild, params GameType[] gameTypes)
		{
			Read(lines.ToArray());
			State.Replay.Version = Version;
			State.Replay.Build = hsBuild.ToString();
			for(var i = 0; i < State.Replay.Games.Count; i++)
			{
				if(gameTypes.Length == 1)
					State.Replay.Games[i].Type = (int)gameTypes[0];
				else
					State.Replay.Games[i].Type = gameTypes.Length > i ? (int)gameTypes[i] : 0;
			}
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
				case "GameState.DebugPrintEntityChoices":
                    ChoicesHandler.Handle(timestamp, data, State);
					break;
				case "GameState.DebugPrintEntitiesChosen":
					EntityChosenHandler.Handle(timestamp, data, State);
					break;
                case "GameState.DebugPrintOptions":
					OptionsHandler.Handle(timestamp, data, State);
					break;
				case "GameState.SendOption":
					SendOptionHandler.Handle(timestamp, data, State);
					break;
				case "GameState.OnEntityChoices":
					// Spectator mode noise
					break;
				case "ChoiceCardMgr.WaitThenShowChoices":
					// Not needed for replays
					break;
				case "GameState.DebugPrintChoice":
					Console.WriteLine("Warning: DebugPrintChoice was removed in 10357. Ignoring.");
                    break;
				default:
					if(!method.StartsWith("PowerTaskList.") && !method.StartsWith("PowerProcessor.") && !method.StartsWith("PowerSpellController"))
						Console.WriteLine("Warning: Unhandled method: " + method);
					break;
			}
		}
	}
}