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

#endregion

namespace HearthstoneReplays.Replay
{
	public class Replay
	{
		private readonly Dictionary<int, Entity> _entities = new Dictionary<int, Entity>();
		private readonly HearthstoneReplay _replay;
		public readonly List<Action> Actions = new List<Action>();
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
			_index = -1;
		}


	    private Action GetActionAtIndex(int index)
	    {
	        return GetActionAtIndex(index, Actions);
	    }
        private Action GetActionAtIndex(int index, List<Action> actions)
	    {
            foreach (var action in actions)
            {
                if (index <= 0)
                    return action;
                index--;
                var subAction = GetActionAtIndex(index, action.SubActions);
                if (subAction != null)
                    return subAction;
                index -= action.SubActions.Count;
            }
            return null;
	    }

		public Action GetNextAction()
		{
            return GetActionAtIndex(++_index);
			if(_index >= Actions.Count - 1)
				return null;
			return Actions[++_index];
		}

		public Action GetNextAction(ActionType type)
		{
		    Action action;
		    do
		    {
		        action = GetActionAtIndex(++_index);
		    } while (action != null && action.Type != type);
		    return action;

			if(_index >= Actions.Count - 1)
				return null;
			do
			{
				_index++;
				if(_index >= Actions.Count - 1)
					return null;
			} while(Actions[_index].Type != type);

			return Actions[_index].Type == type ? Actions[_index] : null;
		}

	    public Action GetPreviousAction()
        {
            return GetActionAtIndex(--_index);
            if (_index <= 0)
	            return null;
	        return Actions[--_index];
	    }

        public Action GetPreviousAction(ActionType type)
        {
            Action action;
            do
            {
                action = GetActionAtIndex(--_index);
            } while(action != null && action.Type != type);
            return action;
            if(_index < 0)
                return null;
            do
            {
                _index--;
                if(_index < 0)
                    return null;
            } while(Actions[_index].Type != type);

            return Actions[_index].Type == type ? Actions[_index] : null;
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
				AnalyzeGameData(data, Actions, 0);

			var localPlayer =
				Actions.FirstOrDefault(
				                          action =>
				                          (action.GameState.Player1.Hand.All(x => !string.IsNullOrEmpty(x.CardId)) &&
				                           action.GameState.Player2.Hand.All(x => string.IsNullOrEmpty(x.CardId))) ||
				                          (action.GameState.Player1.Hand.All(x => string.IsNullOrEmpty(x.CardId)) &&
				                           action.GameState.Player2.Hand.All(x => !string.IsNullOrEmpty(x.CardId))));
			if(localPlayer == null)
				throw new Exception("Could not determine local player");

			var p1IsLocal = localPlayer.GameState.Player1.Hand.All(x => !string.IsNullOrEmpty(x.CardId)) &&
			                localPlayer.GameState.Player2.Hand.All(x => string.IsNullOrEmpty(x.CardId));
		    Action gs;
		    int count = 0;
		    while ((gs = GetActionAtIndex(count++)) != null)
            {
                gs.GameState.LocalPlayer = p1IsLocal ? gs.GameState.Player1 : gs.GameState.Player2;
                gs.GameState.Opponent = p1IsLocal ? gs.GameState.Player2 : gs.GameState.Player1;
            }
		}

	    private void AddGameState(List<Action> actions, ActionType type, int level, int source, int target = 0)
        {
            var action = new Action((Dictionary<int, Entity>)Utility.DeepClone(_entities), type, source, target, level);
            actions.Add(action);
        }

		private void AnalyzeGameData(GameData data, List<Action> actions, int level)
		{
			var action = data as ReplayData.GameActions.Action;
			if(action != null)
			{
			    ActionType startType, endType;
			    switch ((POWER_SUBTYPE) action.Type)
			    {
			        case POWER_SUBTYPE.PLAY:
			            startType = ActionType.ActionStartPlay;
			            endType = ActionType.ActionEndPlay;
			            break;
			        case POWER_SUBTYPE.ATTACK:
			            startType = ActionType.ActionStartAttack;
			            endType = ActionType.ActionEndAttack;
			            break;
			        case POWER_SUBTYPE.DEATHS:
			            startType = ActionType.ActionStartDeaths;
			            endType = ActionType.ActionEndDeaths;
			            break;
			        case POWER_SUBTYPE.FATIGUE:
			            startType = ActionType.ActionStartFatigue;
			            endType = ActionType.ActionEndFatigue;
			            break;
			        case POWER_SUBTYPE.JOUST:
			            startType = ActionType.ActionStartJoust;
			            endType = ActionType.ActionEndJoust;
			            break;
			        case POWER_SUBTYPE.POWER:
			            startType = ActionType.ActionStartPower;
			            endType = ActionType.ActionEndPower;
			            break;
			        case POWER_SUBTYPE.TRIGGER:
			            startType = ActionType.ActionStartTrigger;
			            endType = ActionType.ActionEndTrigger;
			            break;
			        default:
			            startType = ActionType.ActionStartUnknown;
			            endType = ActionType.ActionEndUnknown;
			            break;
			    }

			    var startSubAction = new Action((Dictionary<int, Entity>)Utility.DeepClone(_entities), startType, action.Entity, action.Target, level);
                actions.Add(startSubAction);
                foreach(var subData in action.Data)
					AnalyzeGameData(subData, startSubAction.SubActions, level + 1);
			    if (startSubAction.SubActions.Count == 0)
			        actions.Remove(startSubAction);
			    else
                {
                    var endSubAction = new Action((Dictionary<int, Entity>)Utility.DeepClone(_entities), endType, action.Entity, action.Target, level);
                    actions.Add(endSubAction);
                }
            }

			var tagChange = data as TagChange;
		    if (tagChange != null)
		    {
		        var prevValue = _entities[tagChange.Entity].GetTag((GAME_TAG) tagChange.Name);
		        if (prevValue == tagChange.Value)
		            return;
		        _entities[tagChange.Entity].SetTag((GAME_TAG) tagChange.Name, tagChange.Value);

		        switch (tagChange.Name)
		        {
		            case (int) GAME_TAG.CURRENT_PLAYER:
		                if (prevValue != tagChange.Value && tagChange.Value == 1)
		                    AddGameState(actions, ActionType.TurnStart, level, tagChange.Entity);
		                break;
		            case (int) GAME_TAG.PLAYSTATE:
		                if (tagChange.Value == (int) TAG_PLAYSTATE.WON)
		                    AddGameState(actions, ActionType.Victory, level, tagChange.Entity);
		                else if (tagChange.Value == (int) TAG_PLAYSTATE.LOST)
		                    AddGameState(actions, ActionType.Loss, level, tagChange.Entity);
		                else if (tagChange.Value == (int) TAG_PLAYSTATE.TIED)
		                    AddGameState(actions, ActionType.Tie, level, tagChange.Entity);
		                break;
		            case (int) GAME_TAG.DAMAGE:
		                if (tagChange.Value > 0)
		                    AddGameState(actions, ActionType.Damage, level, tagChange.Entity);
		                break;
		            case (int) GAME_TAG.ZONE:
		                switch (prevValue)
		                {
		                    case (int) TAG_ZONE.HAND:
		                        if (tagChange.Value == (int) TAG_ZONE.DECK &&
		                            _entities[2].GetTag(GAME_TAG.MULLIGAN_STATE) != (int) TAG_MULLIGAN.DONE
		                            && _entities[3].GetTag(GAME_TAG.MULLIGAN_STATE) != (int) TAG_MULLIGAN.DONE)
		                            AddGameState(actions, ActionType.Mulligan, level, tagChange.Entity);
		                        else if (tagChange.Value == (int) TAG_ZONE.PLAY)
		                            AddGameState(actions, ActionType.Play, level, tagChange.Entity);
		                        else
		                            AddGameState(actions, ActionType.HandDiscard, level, tagChange.Entity);
		                        break;
		                    case (int) TAG_ZONE.DECK:
		                        if (tagChange.Value == (int) TAG_ZONE.HAND)
		                            AddGameState(actions, ActionType.Draw, level, tagChange.Entity);
		                        else if (tagChange.Value == (int) TAG_ZONE.PLAY || tagChange.Value == (int) TAG_ZONE.SECRET)
		                            AddGameState(actions, ActionType.PlayFromDeck, level, tagChange.Entity);
		                        else
		                            AddGameState(actions, ActionType.DeckDiscard, level, tagChange.Entity);
		                        break;
		                    case (int) TAG_ZONE.PLAY:

		                        if (tagChange.Value == (int) TAG_ZONE.GRAVEYARD)
		                            AddGameState(actions, ActionType.Death, level, tagChange.Entity);
		                        else if (tagChange.Value == (int) TAG_ZONE.HAND)
		                            AddGameState(actions, ActionType.PlayToHand, level, tagChange.Entity);
		                        else if (tagChange.Value == (int) TAG_ZONE.DECK)
		                            AddGameState(actions, ActionType.PlayToDeck, level, tagChange.Entity);
		                        else
		                            AddGameState(actions, ActionType.UnknownZoneChangeTC, level, tagChange.Entity);
		                        break;
		                    case (int) TAG_ZONE.SECRET:
		                        if (tagChange.Value == (int) TAG_ZONE.GRAVEYARD)
		                            AddGameState(actions, ActionType.SecretTrigger, level, tagChange.Entity);
		                        else
		                            AddGameState(actions, ActionType.UnknownZoneChangeTC, level, tagChange.Entity);
		                        break;
		                    case (int) TAG_ZONE.INVALID:
		                        if (tagChange.Value == (int) TAG_ZONE.HAND)
		                            AddGameState(actions, ActionType.CreateInHand, level, tagChange.Entity);
		                        else if (tagChange.Value == (int) TAG_ZONE.PLAY)
		                            AddGameState(actions, ActionType.CreateInPlay, level, tagChange.Entity);
		                        else if (tagChange.Value == (int) TAG_ZONE.DECK)
		                            AddGameState(actions, ActionType.CreateInDeck, level, tagChange.Entity);
		                        else
		                            AddGameState(actions, ActionType.UnknownZoneChangeTC, level, tagChange.Entity);
		                        break;
		                    default:
		                        AddGameState(actions, ActionType.UnknownZoneChangeTC, level, tagChange.Entity);
		                        break;
		                }
		                break;
		            case (int) GAME_TAG.ATTACKING:
		                Attacking(tagChange.Value == 0 ? null : (int?) tagChange.Entity, actions, level);
		                break;
		            case (int) GAME_TAG.DEFENDING:
		                Defending(tagChange.Value == 0 ? null : (int?) tagChange.Entity, actions, level);
		                break;
		            case (int) GAME_TAG.CONTROLLER:
		                AddGameState(actions, ActionType.Steal, level, tagChange.Entity);
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
                        if (prevValue == (int) TAG_ZONE.HAND)
                        {
                            if(tag.Value == (int)TAG_ZONE.PLAY)
                                AddGameState(actions, ActionType.Play, level, showEntity.Entity);
                            else
                                AddGameState(actions, ActionType.HandDiscard, level, showEntity.Entity);
                        }
                        else if(prevValue == (int)TAG_ZONE.PLAY && tag.Value == (int)TAG_ZONE.GRAVEYARD)
                            AddGameState(actions, ActionType.Death, level, showEntity.Entity);
                        else
                            AddGameState(actions, ActionType.UnknownZoneChangeT, level, showEntity.Entity);
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
        private void Attacking(int? entity, List<Action> actions, int level)
        {
            _attackingEntity = entity;
            if(_attackingEntity.HasValue && _defendingEntity.HasValue)
                AddGameState(actions, ActionType.Attack, level, _attackingEntity.Value, _defendingEntity.Value);
        }

        private int? _defendingEntity;
        private void Defending(int? entity, List<Action> actions, int level)
        {
            _defendingEntity = entity;
            if(_attackingEntity.HasValue && _defendingEntity.HasValue)
                AddGameState(actions, ActionType.Attack, level, _attackingEntity.Value, _defendingEntity.Value);
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