#region

using System;
using System.Collections.Generic;
using System.Linq;
using HearthstoneReplays.Hearthstone.Enums;

#endregion

namespace HearthstoneReplays.Replay
{
	public class GameState
	{
		public Dictionary<int, Entity> AllEntities { get; }
		public TimeSpan GameTime;
		public Player Player1 { get; }
		public Player Player2 { get; }
		public ActionType Type { get; }
	    public Entity Source { get; }

		public GameState(Dictionary<int, Entity> entities, ActionType type, int source)
		{
			AllEntities = entities;
			Type = type;
			Player1 = new Player(entities, 1);
			Player2 = new Player(entities, 2);
		    Source = entities[source];
		}

		public Player LocalPlayer { get; set; }
		public Player Opponent { get; set; }
	    public Player ActivePlayer
	    {
	        get { return Player1.PlayerEntity.GetTag(GAME_TAG.CURRENT_PLAYER) == 1 ? Player1 : Player2; }
	    }

	    public override string ToString()
		{
			var p1Board = Player1.Board.Any() ? Player1.Board.Select(x => x.CardId).Aggregate((c, n) => c + ", " + n) : "";
			var p1Hand = Player1.Hand.Any() ? Player1.Hand.Select(x => x.CardId).Aggregate((c, n) => c + ", " + n) : "";
			var p2Board = Player2.Board.Any() ? Player2.Board.Select(x => x.CardId).Aggregate((c, n) => c + ", " + n) : "";
			var p2Hand = Player2.Hand.Any() ? Player2.Hand.Select(x => x.CardId).Aggregate((c, n) => c + ", " + n) : "";
	        var name = string.IsNullOrEmpty(Source.Name) ? Source.CardId : Source.Name;
	        var player = ActivePlayer == LocalPlayer ? "Player" : "Opponent";
            return string.Format("({0}) {1} {2} {3}", AllEntities[1].GetTag(GAME_TAG.TURN), player, name, Type);
            //return string.Format("[{0} Turn {1}:{2}]P1: Board[{3}] - Hand[{4}] | P2: Board[{5}] - Hand[{6}]", name, AllEntities[1].GetTag(GAME_TAG.TURN),
			  //                   Type, p1Board, p1Hand, p2Board, p2Hand);
		}
	}

	public class Player
	{
		public int Id;

		public Player(Dictionary<int, Entity> allEntities, int id)
		{
			Id = id;
			var playerEntites = allEntities.Values.Where(e => e.GetTag(GAME_TAG.CONTROLLER) == id).ToList();
			Hero = playerEntites.FirstOrDefault(e => !string.IsNullOrEmpty(e.CardId) && e.CardId.StartsWith("HERO_"));
			PlayerEntity = playerEntites.FirstOrDefault(e => e.HasTag(GAME_TAG.PLAYER_ID));
			Board = playerEntites.Where(e => e.IsInZone(TAG_ZONE.PLAY)).ToList();
			Hand = playerEntites.Where(e => e.IsInZone(TAG_ZONE.HAND)).ToList();
			Deck = playerEntites.Where(e => e.IsInZone(TAG_ZONE.DECK)).ToList();
			SetAside = playerEntites.Where(e => e.IsInZone(TAG_ZONE.SETASIDE)).ToList();
			Invalid = playerEntites.Where(e => e.IsInZone(TAG_ZONE.INVALID)).ToList();
			Graveyard = playerEntites.Where(e => e.IsInZone(TAG_ZONE.GRAVEYARD)).ToList();
			RemovedFromGame = playerEntites.Where(e => e.IsInZone(TAG_ZONE.REMOVEDFROMGAME)).ToList();
			Secret = playerEntites.Where(e => e.IsInZone(TAG_ZONE.SECRET)).ToList();
		}

		public List<Entity> Board { get; private set; }
		public List<Entity> Hand { get; private set; }
		public List<Entity> Deck { get; private set; }
		public List<Entity> SetAside { get; private set; }
		public List<Entity> Invalid { get; private set; }
		public List<Entity> Graveyard { get; private set; }
		public List<Entity> RemovedFromGame { get; private set; }
		public List<Entity> Secret { get; private set; }
		public Entity Hero { get; private set; }
		public Entity PlayerEntity { get; private set; }
	}
}