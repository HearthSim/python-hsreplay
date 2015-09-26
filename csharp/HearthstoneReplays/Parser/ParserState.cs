#region

using HearthstoneReplays.ReplayData;
using HearthstoneReplays.ReplayData.Meta;
using HearthstoneReplays.ReplayData.Meta.Options;

#endregion

namespace HearthstoneReplays.Parser
{
	public class ParserState
	{
		public ParserState()
		{
			Reset();
		}

		public HearthstoneReplay Replay { get; set; }
		public Game CurrentGame { get; set; }
		public Node Node { get; set; }
		public GameData GameData { get; set; }
		public SendChoices SendChoices { get; set; }
		public Choices Choices { get; set; }
		public Options Options { get; set; }
		public Option CurrentOption { get; set; }
		public object LastOption { get; set; }
		public int FirstPlayerId { get; set; }
	    public int CurrentPlayerId { get; set; }

		public void Reset()
		{
			Replay = new HearthstoneReplay();
			CurrentGame = new Game();
		}
	}
}