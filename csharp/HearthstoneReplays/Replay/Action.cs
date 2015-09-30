using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using HearthstoneReplays.Hearthstone.Enums;

namespace HearthstoneReplays.Replay
{
    public class Action
    {
        public GameState GameState { get; private set; }
        public List<Action> SubActions { get; private set; }
        public ActionType Type { get; private set; }
        public Entity Source { get; private set; }
        public Entity Target { get; private set; }
        public int Level { get; private set; }

        public Action(Dictionary<int, Entity> entities, ActionType type, int source = 0, int target = 0, int level = 0)
        {
            GameState = new GameState(entities);
            Type = type;
            if(source != 0)
                Source = entities[source];
            if(target != 0)
                Target = entities[target];
            SubActions = new List<Action>();
            Level = level;
        }


        public override string ToString()
        {
            var source = Source != null ? " " + (string.IsNullOrEmpty(Source.Name) ? Source.CardId : Source.Name) : "";
            var target = Target != null ? " -> " + (string.IsNullOrEmpty(Target.Name) ? Target.CardId : Target.Name) : "";
            var player = GameState.ActivePlayer == GameState.LocalPlayer ? "Player" : "Opponent";
            return new string('\t', Level) + string.Format("({0}) {1} {2}{3}{4}", GameState.AllEntities[1].GetTag(GAME_TAG.TURN), Type, player, source, target);
            //var p1Board = Player1.Board.Any() ? Player1.Board.Select(x => x.CardId).Aggregate((c, n) => c + ", " + n) : "";
            //var p1Hand = Player1.Hand.Any() ? Player1.Hand.Select(x => x.CardId).Aggregate((c, n) => c + ", " + n) : "";
            //var p2Board = Player2.Board.Any() ? Player2.Board.Select(x => x.CardId).Aggregate((c, n) => c + ", " + n) : "";
            //var p2Hand = Player2.Hand.Any() ? Player2.Hand.Select(x => x.CardId).Aggregate((c, n) => c + ", " + n) : "";
            //return string.Format("[{0} Turn {1}:{2}]P1: Board[{3}] - Hand[{4}] | P2: Board[{5}] - Hand[{6}]", name, AllEntities[1].GetTag(GAME_TAG.TURN),
            //                   Type, p1Board, p1Hand, p2Board, p2Hand);
        }
    }
}
