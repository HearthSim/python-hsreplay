#region

using System;
using System.Linq;
using HearthstoneReplays;
using HearthstoneReplays.Hearthstone.Enums;
using HearthstoneReplays.Parser;
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
            var replayData = ReplayParser.FromTextReader(TestDataReader.GetInputFile("Power_2.log.txt"));
            //var replayData = ReplaySerializer.Deserialize(TestDataReader.GetInputFile("Power_2.log.xml"));
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
        public void CorrectLocalPlayerAndOpponentTest()
        {
            Assert.AreEqual("Veritas", _replay.GameStates.First().LocalPlayer.PlayerEntity.Name);
            Assert.AreEqual("Veritas", _replay.GameStates.Last().LocalPlayer.PlayerEntity.Name);
            Assert.AreEqual("TheKEG", _replay.GameStates.First().Opponent.PlayerEntity.Name);
            Assert.AreEqual("TheKEG", _replay.GameStates.Last().Opponent.PlayerEntity.Name);
        }

        [TestMethod]
        public void CorrectPlayerEntityIdTest()
        {
            Assert.AreEqual("TheKEG", _replay.GameStates.First().AllEntities.First(e => e.Value.Id == 2).Value.Name);
            Assert.AreEqual("TheKEG", _replay.GameStates.Last().AllEntities.First(e => e.Value.Id == 2).Value.Name);
            Assert.AreEqual("Veritas", _replay.GameStates.First().AllEntities.First(e => e.Value.Id == 3).Value.Name);
            Assert.AreEqual("Veritas", _replay.GameStates.Last().AllEntities.First(e => e.Value.Id == 3).Value.Name);
        }

        [TestMethod]
        public void ActionTypeTurnStartTest()
        {
            var firstTurn = _replay.GetNextAction(ActionType.TurnStart);
            Assert.IsNotNull(firstTurn);
            Assert.AreEqual(1, firstTurn.Player1.PlayerEntity.GetTag(GAME_TAG.RESOURCES));
            Assert.AreEqual(0, firstTurn.Player2.PlayerEntity.GetTag(GAME_TAG.RESOURCES));
            var secondTurn = _replay.GetNextAction(ActionType.TurnStart);
            Assert.IsNotNull(secondTurn);
            Assert.AreEqual(1, secondTurn.Player1.PlayerEntity.GetTag(GAME_TAG.RESOURCES));
            Assert.AreEqual(1, secondTurn.Player2.PlayerEntity.GetTag(GAME_TAG.RESOURCES));
            var thirdTurn = _replay.GetNextAction(ActionType.TurnStart);
            Assert.IsNotNull(thirdTurn);
            Assert.AreEqual(2, thirdTurn.Player1.PlayerEntity.GetTag(GAME_TAG.RESOURCES));
            Assert.AreEqual(1, thirdTurn.Player2.PlayerEntity.GetTag(GAME_TAG.RESOURCES));
            var fourthTurn = _replay.GetNextAction(ActionType.TurnStart);
            Assert.IsNotNull(fourthTurn);
            Assert.AreEqual(2, fourthTurn.Player1.PlayerEntity.GetTag(GAME_TAG.RESOURCES));
            Assert.AreEqual(2, fourthTurn.Player2.PlayerEntity.GetTag(GAME_TAG.RESOURCES));
        }

        [TestMethod]
        public void ActionTypePlay_LessCardsAfterPlayTest()
        {
            GameState play;
            while((play = _replay.GetNextAction(ActionType.Play)) != null)
            {
                var prePlay = _replay.GetPreviousAction();
                _replay.GetNextAction();
                Assert.IsTrue(prePlay.ActivePlayer.Hand.Count > play.ActivePlayer.Hand.Count);
            }
        }

        [TestMethod]
        public void ActionTypeDraw_MoreCardsAfterDrawTest()
        {
            GameState draw;
            while ((draw = _replay.GetNextAction(ActionType.Draw)) != null)
            {
                var preDraw = _replay.GetPreviousAction();
                _replay.GetNextAction();
                Assert.IsTrue(preDraw.ActivePlayer.Hand.Count < draw.ActivePlayer.Hand.Count);
            }
        }

        [TestMethod]
        public void LogAllTheThings()
        {
            GameState draw;
            while((draw = _replay.GetNextAction()) != null)
            {
                Console.WriteLine(draw);
            }
        }
    }
}