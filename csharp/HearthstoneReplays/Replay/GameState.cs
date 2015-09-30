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
		public Dictionary<int, Entity> AllEntities { get; private set; }
		public TimeSpan GameTime;
		public Player Player1 { get; private set; }
		public Player Player2 { get; private set; }

		public GameState(Dictionary<int, Entity> entities)
		{
			AllEntities = entities;
            Player1 = new Player(entities, 1);
			Player2 = new Player(entities, 2);
		}

		public Player LocalPlayer { get; set; }
		public Player Opponent { get; set; }
	    public Player ActivePlayer
	    {
	        get { return Player1.PlayerEntity.GetTag(GAME_TAG.CURRENT_PLAYER) == 1 ? Player1 : Player2; }
	    }

	}
}