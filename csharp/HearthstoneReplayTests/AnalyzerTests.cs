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
			var replayData = ReplaySerializer.Deserialize(TestDataReader.GetInputFile("Power_2.log.xml"));
			_replay = new Replay(replayData);
			_replay.LoadGame(0);
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
			while((gState = _replay.GetNextAction(ActionType.Play)) != null)
			{
				foreach(var x in gState.LocalPlayer.Hand)
					Assert.IsFalse(string.IsNullOrEmpty(x.CardId), gState.ToString());
			}
		}

		[TestMethod]
		public void OpponentHandCardIdsTest()
		{
			GameState gState;
			while((gState = _replay.GetNextAction(ActionType.Play)) != null)
			{
				foreach(var x in gState.Opponent.Hand)
					Assert.IsTrue(string.IsNullOrEmpty(x.CardId), gState.ToString());
			}
		}

		[TestMethod]
		public void PlayerBoardCardIdsTest()
		{
			GameState gState;
			while((gState = _replay.GetNextAction(ActionType.Play)) != null)
			{
				foreach(var x in gState.LocalPlayer.Board.Where(e => e.IsOfType(TAG_CARDTYPE.MINION)))
					Assert.IsFalse(string.IsNullOrEmpty(x.CardId), gState.ToString());
			}
		}

		[TestMethod]
		public void OpponentBoardCardIdsTest()
		{
			GameState gState;
			while((gState = _replay.GetNextAction(ActionType.Play)) != null)
			{
				foreach(var x in gState.Opponent.Board.Where(e => e.IsOfType(TAG_CARDTYPE.MINION)))
					Assert.IsFalse(string.IsNullOrEmpty(x.CardId), gState.ToString());
			}
		}

	    [TestMethod]
	    public void GameHasWinnerTest()
        {
            var playerWon = _replay.GameStates.Last().LocalPlayer.PlayerEntity.GetTag(GAME_TAG.PLAYSTATE) == (int)TAG_PLAYSTATE.WON;
            var opponentWon = _replay.GameStates.Last().Opponent.PlayerEntity.GetTag(GAME_TAG.PLAYSTATE) == (int)TAG_PLAYSTATE.WON;
            Assert.IsTrue(playerWon || opponentWon);
        }

        [TestMethod]
        public void CorrectLocalPlayer()
        {
            var playerName = _replay.GameStates.Last().LocalPlayer.PlayerEntity.Name;
            Assert.AreEqual(playerName, "Veritas");
        }

        [TestMethod]
        public void Something()
        {
            var firstTurn = _replay.GetNextAction(ActionType.TurnStart);
            Assert.IsNotNull(firstTurn);
            //var playerName = _replay.GetNextAction();
            //Assert.AreEqual(playerName, "Veritas");
        }
    }
}