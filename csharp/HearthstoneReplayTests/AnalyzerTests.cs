#region

using System.Linq;
using HearthstoneReplays;
using HearthstoneReplays.Hearthstone.Enums;
using HearthstoneReplays.Replay;
using Microsoft.VisualStudio.TestTools.UnitTesting;

#endregion

namespace HearthstoneReplayTests
{
	[TestClass]
	public class AnalyzerTests
	{
		private static Replay _replay;

		[ClassInitialize]
		public static void Setup(TestContext context)
		{
			var replayData = ReplaySerializer.Deserialize(TestDataReader.GetInputFile("Power_1.log.xml"));
			_replay = new Replay(replayData);
			_replay.LoadGame(1);
		}

		[TestInitialize]
		public void TestInitialize()
		{
			_replay.Reset();
		}

		[TestMethod]
		public void PlayerHandCardIdsTest()
		{
			GameState gState;
			while((gState = _replay.GetNextAction(GameStateType.PLAY)) != null)
			{
				foreach(var x in gState.LocalPlayer.Hand)
					Assert.IsFalse(string.IsNullOrEmpty(x.CardId), gState.ToString());
			}
		}

		[TestMethod]
		public void OpponentHandCardIdsTest()
		{
			GameState gState;
			while((gState = _replay.GetNextAction(GameStateType.PLAY)) != null)
			{
				foreach(var x in gState.Opponent.Hand)
					Assert.IsTrue(string.IsNullOrEmpty(x.CardId), gState.ToString());
			}
		}

		[TestMethod]
		public void PlayerBoardCardIdsTest()
		{
			GameState gState;
			while((gState = _replay.GetNextAction(GameStateType.PLAY)) != null)
			{
				foreach(var x in gState.LocalPlayer.Board.Where(e => e.IsOfType(TAG_CARDTYPE.MINION)))
					Assert.IsFalse(string.IsNullOrEmpty(x.CardId), gState.ToString());
			}
		}

		[TestMethod]
		public void OpponentBoardCardIdsTest()
		{
			GameState gState;
			while((gState = _replay.GetNextAction(GameStateType.PLAY)) != null)
			{
				foreach(var x in gState.Opponent.Board.Where(e => e.IsOfType(TAG_CARDTYPE.MINION)))
					Assert.IsFalse(string.IsNullOrEmpty(x.CardId), gState.ToString());
			}
		}
	}
}