using System.Collections.Generic;
using System.Linq;
using HearthDb.Enums;

namespace HearthstoneReplays.Replay
{
    public class Player
    {
        public int Id;

        public Player(Dictionary<int, Entity> allEntities, int id)
        {
            Id = id;
            var playerEntites = allEntities.Values.Where(e => e.GetTag(GameTag.CONTROLLER) == id).ToList();
            Hero = playerEntites.FirstOrDefault(e => !string.IsNullOrEmpty(e.CardId) && e.CardId.StartsWith("HERO_"));
            PlayerEntity = playerEntites.FirstOrDefault(e => e.HasTag(GameTag.PLAYER_ID));
            Board = playerEntites.Where(e => e.IsInZone(Zone.PLAY)).ToList();
            Hand = playerEntites.Where(e => e.IsInZone(Zone.HAND)).ToList();
            Deck = playerEntites.Where(e => e.IsInZone(Zone.DECK)).ToList();
            SetAside = playerEntites.Where(e => e.IsInZone(Zone.SETASIDE)).ToList();
            Invalid = playerEntites.Where(e => e.IsInZone(Zone.INVALID)).ToList();
            Graveyard = playerEntites.Where(e => e.IsInZone(Zone.GRAVEYARD)).ToList();
            RemovedFromGame = playerEntites.Where(e => e.IsInZone(Zone.REMOVEDFROMGAME)).ToList();
            Secret = playerEntites.Where(e => e.IsInZone(Zone.SECRET)).ToList();
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