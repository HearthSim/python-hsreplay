#region

using System;
using System.Linq;
using HearthDb.Enums;
using HearthstoneReplays.Parser;
using HearthstoneReplays.Replay;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Action = HearthstoneReplays.Replay.Action;

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
			Action action;
			while((action = _replay.GetNextAction(ActionType.Play)) != null)
			{
				foreach(var x in action.GameState.LocalPlayer.Hand)
					Assert.IsFalse(string.IsNullOrEmpty(x.CardId), action.ToString());
			}
		}

		[TestMethod]
		public void OpponentHandCardIdsTest()
		{
			Action action;
			while((action = _replay.GetNextAction(ActionType.Play)) != null)
			{
				foreach(var x in action.GameState.Opponent.Hand)
					Assert.IsTrue(string.IsNullOrEmpty(x.CardId), action.ToString());
			}
		}

		[TestMethod]
		public void PlayerBoardCardIdsTest()
		{
			Action action;
			while((action = _replay.GetNextAction(ActionType.Play)) != null)
			{
				foreach(var x in action.GameState.LocalPlayer.Board.Where(e => e.IsOfType(CardType.MINION)))
					Assert.IsFalse(string.IsNullOrEmpty(x.CardId), action.ToString());
			}
		}

		[TestMethod]
		public void OpponentBoardCardIdsTest()
		{
			Action action;
			while((action = _replay.GetNextAction(ActionType.Play)) != null)
			{
				foreach(var x in action.GameState.Opponent.Board.Where(e => e.IsOfType(CardType.MINION)))
					Assert.IsFalse(string.IsNullOrEmpty(x.CardId), action.ToString());
			}
		}

	    [TestMethod]
	    public void GameHasWinnerTest()
        {
            var playerWon = _replay.Actions.Last().GameState.LocalPlayer.PlayerEntity.GetTag(GameTag.PLAYSTATE) == (int)PlayState.WON;
            var opponentWon = _replay.Actions.Last().GameState.Opponent.PlayerEntity.GetTag(GameTag.PLAYSTATE) == (int)PlayState.WON;
            Assert.IsTrue(playerWon || opponentWon);
        }

        [TestMethod]
        public void CorrectLocalPlayerAndOpponentTest()
        {
            Assert.AreEqual("Veritas", _replay.Actions.First().GameState.LocalPlayer.PlayerEntity.Name);
            Assert.AreEqual("Veritas", _replay.Actions.Last().GameState.LocalPlayer.PlayerEntity.Name);
            Assert.AreEqual("TheKEG", _replay.Actions.First().GameState.Opponent.PlayerEntity.Name);
            Assert.AreEqual("TheKEG", _replay.Actions.Last().GameState.Opponent.PlayerEntity.Name);
        }

        [TestMethod]
        public void CorrectPlayerEntityIdTest()
        {
            Assert.AreEqual("TheKEG", _replay.Actions.First().GameState.AllEntities.First(e => e.Value.Id == 2).Value.Name);
            Assert.AreEqual("TheKEG", _replay.Actions.Last().GameState.AllEntities.First(e => e.Value.Id == 2).Value.Name);
            Assert.AreEqual("Veritas", _replay.Actions.First().GameState.AllEntities.First(e => e.Value.Id == 3).Value.Name);
            Assert.AreEqual("Veritas", _replay.Actions.Last().GameState.AllEntities.First(e => e.Value.Id == 3).Value.Name);
        }

        [TestMethod]
        public void ActionTypeTurnStartTest()
        {
            var firstTurn = _replay.GetNextAction(ActionType.TurnStart);
            Assert.IsNotNull(firstTurn);
            Assert.AreEqual(1, firstTurn.GameState.Player1.PlayerEntity.GetTag(GameTag.RESOURCES));
            Assert.AreEqual(0, firstTurn.GameState.Player2.PlayerEntity.GetTag(GameTag.RESOURCES));
            var secondTurn = _replay.GetNextAction(ActionType.TurnStart);
            Assert.IsNotNull(secondTurn);
            Assert.AreEqual(1, secondTurn.GameState.Player1.PlayerEntity.GetTag(GameTag.RESOURCES));
            Assert.AreEqual(1, secondTurn.GameState.Player2.PlayerEntity.GetTag(GameTag.RESOURCES));
            var thirdTurn = _replay.GetNextAction(ActionType.TurnStart);
            Assert.IsNotNull(thirdTurn);
            Assert.AreEqual(2, thirdTurn.GameState.Player1.PlayerEntity.GetTag(GameTag.RESOURCES));
            Assert.AreEqual(1, thirdTurn.GameState.Player2.PlayerEntity.GetTag(GameTag.RESOURCES));
            var fourthTurn = _replay.GetNextAction(ActionType.TurnStart);
            Assert.IsNotNull(fourthTurn);
            Assert.AreEqual(2, fourthTurn.GameState.Player1.PlayerEntity.GetTag(GameTag.RESOURCES));
            Assert.AreEqual(2, fourthTurn.GameState.Player2.PlayerEntity.GetTag(GameTag.RESOURCES));
        }

        [TestMethod]
        public void ActionTypePlay_LessCardsAfterPlayTest()
        {
            Action play;
            while((play = _replay.GetNextAction(ActionType.Play)) != null)
            {
                var prePlay = _replay.GetPreviousAction();
                _replay.GetNextAction();
                Assert.IsTrue(prePlay.GameState.ActivePlayer.Hand.Count > play.GameState.ActivePlayer.Hand.Count);
            }
        }

        [TestMethod]
        public void ActionTypeDraw_MoreCardsAfterDrawTest()
        {
            Action draw;
            while ((draw = _replay.GetNextAction(ActionType.Draw)) != null)
            {
                var preDraw = _replay.GetPreviousAction();
                _replay.GetNextAction();
                Assert.IsTrue(preDraw.GameState.ActivePlayer.Hand.Count < draw.GameState.ActivePlayer.Hand.Count);
            }
        }

        [TestMethod]
        public void LogAllTheThings()
        {
            Action draw;
            while((draw = _replay.GetNextAction()) != null)
            {
                Console.WriteLine(draw);
            }
        }
    }
}