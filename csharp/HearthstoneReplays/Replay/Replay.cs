#region

using System;
using System.Collections.Generic;
using System.Linq;
using HearthstoneReplays.Hearthstone.Enums;
using HearthstoneReplays.ReplayData;
using HearthstoneReplays.ReplayData.Entities;
using HearthstoneReplays.ReplayData.GameActions;
using HearthstoneReplays.ReplayData.Meta;
using HearthstoneReplays.ReplayData.Meta.Options;
using Action = HearthstoneReplays.ReplayData.GameActions.Action;

#endregion

namespace HearthstoneReplays.Replay
{
	public class Replay
	{
		private readonly Dictionary<int, Entity> _entities = new Dictionary<int, Entity>();
		private readonly HearthstoneReplay _replay;
		public readonly List<GameState> GameStates = new List<GameState>();
		private GameEntity _gameEntity;
		private int _index;
		private PlayerEntity _p1Entity;
		private PlayerEntity _p2Entity;

		public Replay(HearthstoneReplay replay)
		{
			_replay = replay;
		}

		public Replay(string filePath)
		{
			_replay = ReplaySerializer.Deserialize(filePath);
		}

		public int GetGames
		{
			get { return _replay.Games.Count; }
		}

		public void LoadGame()
		{
			LoadGame(0);
		}

		public void LoadGame(int index)
		{
			AnalyzeReplayData(index);
			Reset();
		}

		public void Reset()
		{
			_index = 0;
		}

		public GameState GetNextAction()
		{
			if(_index >= GameStates.Count - 1)
				return null;
			return GameStates[++_index];
		}

		public GameState GetNextAction(ActionType type)
		{
			if(_index >= GameStates.Count - 1)
				return null;
			do
			{
				_index++;
				if(_index >= GameStates.Count - 1)
					return null;
			} while(GameStates[_index].Type != type);

			return GameStates[_index].Type == type ? GameStates[_index] : null;
		}

	    public GameState GetPreviousAction()
	    {
	        if (_index <= 0)
	            return null;
	        return GameStates[--_index];
	    }

        public GameState GetPreviousAction(ActionType type)
        {
            if(_index < 0)
                return null;
            do
            {
                _index--;
                if(_index < 0)
                    return null;
            } while(GameStates[_index].Type != type);

            return GameStates[_index].Type == type ? GameStates[_index] : null;
        }

		private void AnalyzeReplayData(int index)
		{
			_entities.Clear();
			var game = _replay.Games.ElementAtOrDefault(index);
			if(game == null)
				return;
			var gameEntity = game.Data[0] as GameEntity;
			if(gameEntity == null)
				throw new Exception("No Game Entity");
			_gameEntity = gameEntity;
			_entities.Add(gameEntity.Id, new Entity(gameEntity.Id, tags: gameEntity.Tags) {Name = "GameEntity"});


			var p1 = game.Data[1] as PlayerEntity;
			if(p1 == null)
				throw new Exception("No Player1 Entity");
			_p1Entity = p1;
			_entities.Add(p1.Id, new Entity(p1.Id, p1.Tags, p1.PlayerId) {Name = p1.Name});

			var p2 = game.Data[2] as PlayerEntity;
			if(p2 == null)
				throw new Exception("No Player2 Entity");
			_p2Entity = p2;
		    _entities.Add(p2.Id, new Entity(p2.Id, p2.Tags, p2.PlayerId) {Name = p2.Name});


			foreach(var data in game.Data.Skip(3))
				AnalyzeGameData(data);

			var localPlayer =
				GameStates.FirstOrDefault(
				                          state =>
				                          (state.Player1.Hand.All(x => !string.IsNullOrEmpty(x.CardId)) &&
				                           state.Player2.Hand.All(x => string.IsNullOrEmpty(x.CardId))) ||
				                          (state.Player1.Hand.All(x => string.IsNullOrEmpty(x.CardId)) &&
				                           state.Player2.Hand.All(x => !string.IsNullOrEmpty(x.CardId))));
			if(localPlayer == null)
				throw new Exception("Could not determine local player");

			var p1IsLocal = localPlayer.Player1.Hand.All(x => !string.IsNullOrEmpty(x.CardId)) &&
			                localPlayer.Player2.Hand.All(x => string.IsNullOrEmpty(x.CardId));
			foreach(var gs in GameStates)
			{
				gs.LocalPlayer = p1IsLocal ? gs.Player1 : gs.Player2;
				gs.Opponent = p1IsLocal ? gs.Player2 : gs.Player1;
			}
		}

	    private void AddGameState(ActionType type, int source)
        {
            var gState = new GameState((Dictionary<int, Entity>)Utility.DeepClone(_entities), type, source);
            GameStates.Add(gState);
        }

		private void AnalyzeGameData(GameData data)
		{
			var action = data as Action;
			if(action != null)
			{
				foreach(var subData in action.Data)
					AnalyzeGameData(subData);

			    /*switch ((POWER_SUBTYPE) action.Type)
			    {
			        case POWER_SUBTYPE.ATTACK:
                        AddGameState(ActionType.Attack);
			            break;
                    case POWER_SUBTYPE.DEATHS:
                        AddGameState(ActionType.Death);
			            break;
			    }*/
			}

			var tagChange = data as TagChange;
			if(tagChange != null)
			{
			    var prevValue = _entities[tagChange.Entity].GetTag((GAME_TAG) tagChange.Name);
				_entities[tagChange.Entity].SetTag((GAME_TAG)tagChange.Name, tagChange.Value);

			    switch (tagChange.Name)
			    {
			        case (int) GAME_TAG.CURRENT_PLAYER:
			            if (prevValue != tagChange.Value && tagChange.Value == 1)
			                AddGameState(ActionType.TurnStart, tagChange.Entity);
			            break;
			        case (int) GAME_TAG.PLAYSTATE:
			            if (tagChange.Value == (int) TAG_PLAYSTATE.WON)
			                AddGameState(ActionType.Victory, tagChange.Entity);
			            else if (tagChange.Value == (int) TAG_PLAYSTATE.LOST)
			                AddGameState(ActionType.Loss, tagChange.Entity);
			            else if (tagChange.Value == (int) TAG_PLAYSTATE.TIED)
			                AddGameState(ActionType.Tie, tagChange.Entity);
			            break;
			        case (int) GAME_TAG.DAMAGE:
			            if (tagChange.Value > 0)
			                AddGameState(ActionType.Damage, tagChange.Entity);
			            break;
			        case (int) GAME_TAG.ZONE:
			            if (tagChange.Value == (int) TAG_ZONE.DECK && prevValue == (int) TAG_ZONE.HAND &&
			                _entities[1].GetTag(GAME_TAG.MULLIGAN_STATE) != (int) TAG_MULLIGAN.DONE)
			            {
			                AddGameState(ActionType.Mulligan, tagChange.Entity);
			            }
			            else if (tagChange.Value == (int) TAG_ZONE.HAND && prevValue == (int) TAG_ZONE.DECK)
			                AddGameState(ActionType.Draw, tagChange.Entity);
			            else if (prevValue == (int) TAG_ZONE.HAND && tagChange.Value == (int) TAG_ZONE.PLAY)
			                AddGameState(ActionType.Play, tagChange.Entity);
			            else if (prevValue == (int) TAG_ZONE.HAND)
			                AddGameState(ActionType.HandDiscard, tagChange.Entity);
			            else if (prevValue == (int) TAG_ZONE.PLAY && tagChange.Value == (int) TAG_ZONE.GRAVEYARD)
			                AddGameState(ActionType.Death, tagChange.Entity);
			            else
			                AddGameState(ActionType.Unknown, tagChange.Entity);
			            break;
			        case (int) GAME_TAG.ATTACKING:
			            Attacking(tagChange.Value == 0 ? null : (int?) tagChange.Entity);
			            break;
			        case (int) GAME_TAG.DEFENDING:
			            Defending(tagChange.Value == 0 ? null : (int?) tagChange.Entity);
			            break;
			        case (int) GAME_TAG.NUM_OPTIONS_PLAYED_THIS_TURN:
			            AddGameState(ActionType.TurnEnd, tagChange.Entity);
			            break;

			    }
			    return;
            }
            
            var fullEntity = data as FullEntity;
			if(fullEntity != null)
			{
				_entities.Add(fullEntity.Id, new Entity(fullEntity.Id, fullEntity.CardId, fullEntity.Tags));
				return;
			}

			var showEntity = data as ShowEntity;
			if(showEntity != null)
			{
				_entities[showEntity.Entity].SetCardId(showEntity.CardId);
			    foreach (var tag in showEntity.Tags)
                {
                    var prevValue = _entities[showEntity.Entity].GetTag((GAME_TAG)tag.Name);
                    _entities[showEntity.Entity].SetTag((GAME_TAG)tag.Name, tag.Value);
                    if (tag.Name == (int)GAME_TAG.ZONE)
                    {
                        if(prevValue == (int)TAG_ZONE.HAND && tag.Value == (int)TAG_ZONE.PLAY)
                            AddGameState(ActionType.Play, showEntity.Entity);
                        else if(prevValue == (int)TAG_ZONE.HAND && tag.Value == (int)TAG_ZONE.PLAY)
                            AddGameState(ActionType.Play, showEntity.Entity);
                        else if(prevValue == (int)TAG_ZONE.HAND)
                            AddGameState(ActionType.HandDiscard, showEntity.Entity);
                        else if(prevValue == (int)TAG_ZONE.PLAY && tag.Value == (int)TAG_ZONE.GRAVEYARD)
                            AddGameState(ActionType.Death, showEntity.Entity);
                        else
                            AddGameState(ActionType.Unknown, showEntity.Entity);
                    }
                }
				return;
			}

			var hideEntity = data as HideEntity;
			if(hideEntity != null)
			{
				_entities[hideEntity.Entity].SetTag((GAME_TAG)hideEntity.TagName, hideEntity.TagValue);
				return;
			}

			var metaData = data as MetaData;
			if(metaData != null)
			{
                /* TODO */
                return;
            }

			var choice = data as Choice;
			if(choice != null)
			{
                /* TODO */
                return;
            }

			var sendChoices = data as SendChoices;
			if(sendChoices != null)
			{
                /* TODO */
                return;
            }

			var choices = data as Choices;
			if(choices != null)
			{
                /* TODO */
                return;
            }

			var option = data as Option;
			if(option != null)
			{
                /* TODO */
                return;
            }


			var subOption = data as SubOption;
			if(subOption != null)
			{
                /* TODO */
                return;
            }

			var target = data as Target;
			if(target != null)
			{
                /* TODO */
                return;
            }

			var options = data as Options;
			if(options != null)
			{
                /* TODO */
                return;
            }

			var sendOption = data as SendOption;
			if(sendOption != null)
			{
				/* TODO */
			    return;
			}

		    var metaInfo = data as Info;
		    if (metaInfo != null)
		    {
		        /* TODO */
		        return;
		    }
        }

        private int? _attackingEntity;
        private void Attacking(int? entity)
        {
            _attackingEntity = entity;
            if(_attackingEntity.HasValue && _defendingEntity.HasValue)
                AddGameState(ActionType.Attack, _attackingEntity.Value);
        }

        private int? _defendingEntity;
        private void Defending(int? entity)
        {
            _defendingEntity = entity;
            if(_attackingEntity.HasValue && _defendingEntity.HasValue)
                AddGameState(ActionType.Attack, _attackingEntity.Value);
        }

        private int GetEntityIdFromString(string entity)
		{
			int entityId;
			if(!int.TryParse(entity, out entityId))
			{
				if(entity == "GameEntity")
					entityId = _gameEntity.Id;
				else
				{
					if(string.IsNullOrEmpty(_entities[_p1Entity.Id].Name))
					{
						entityId = _p1Entity.Id;
						_entities[_p1Entity.Id].Name = entity;
					}
					else if(entity == _entities[_p1Entity.Id].Name)
						entityId = _p1Entity.Id;
					else if(string.IsNullOrEmpty(_entities[_p2Entity.Id].Name))
					{
						entityId = _p2Entity.Id;
						_entities[_p2Entity.Id].Name = entity;
					}
					else if(entity == _entities[_p2Entity.Id].Name)
						entityId = _p2Entity.Id;
					else
						throw new Exception("unknown entity name: " + entity);
				}
			}
			if(!_entities.ContainsKey(entityId))
				_entities.Add(entityId, new Entity(entityId));
			return entityId;
		}
	}
}