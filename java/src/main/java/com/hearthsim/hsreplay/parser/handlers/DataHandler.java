package com.hearthsim.hsreplay.parser.handlers;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.regex.Matcher;

import lombok.extern.slf4j.Slf4j;

import com.hearthsim.hsreplay.enums.GameTag;
import com.hearthsim.hsreplay.enums.MetaDataType;
import com.hearthsim.hsreplay.enums.PowSubType;
import com.hearthsim.hsreplay.parser.Helper;
import com.hearthsim.hsreplay.parser.Node;
import com.hearthsim.hsreplay.parser.ParserState;
import com.hearthsim.hsreplay.parser.Regexes;
import com.hearthsim.hsreplay.parser.Utils;
import com.hearthsim.hsreplay.parser.replaydata.Game;
import com.hearthsim.hsreplay.parser.replaydata.entities.FullEntity;
import com.hearthsim.hsreplay.parser.replaydata.entities.GameEntity;
import com.hearthsim.hsreplay.parser.replaydata.entities.PlayerEntity;
import com.hearthsim.hsreplay.parser.replaydata.gameactions.Action;
import com.hearthsim.hsreplay.parser.replaydata.gameactions.HideEntity;
import com.hearthsim.hsreplay.parser.replaydata.gameactions.ShowEntity;
import com.hearthsim.hsreplay.parser.replaydata.gameactions.Tag;
import com.hearthsim.hsreplay.parser.replaydata.gameactions.TagChange;
import com.hearthsim.hsreplay.parser.replaydata.meta.Info;
import com.hearthsim.hsreplay.parser.replaydata.meta.MetaData;

@Slf4j
public class DataHandler {

	public static void handle(String timestamp, String data, ParserState state) throws Exception {
		String trimmed = data.trim();
		int indentLevel = data.length() - trimmed.length();
		data = trimmed;

		log.info("Considering line " + data);

		if ("ACTION_END".equals(data)) {
			state.setNode(state.getNode().getParent() != null ? state.getNode().getParent() : state.getNode());
			return;
		}

		if ("CREATE_GAME".equals(data)) {
			Game currentGame = Game.builder().data(new ArrayList<>()).timestamp(timestamp).build();
			state.setCurrentGame(currentGame);
			state.getReplay().getGames().add(currentGame);
			Node node = new Node(Game.class, currentGame, 0, null);
			state.setNode(node);
			return;
		}

		Matcher match = Regexes.ActionCreategameRegex.matcher(data);
		if (match.matches()) {
			String id = match.group(1);
			if (Integer.parseInt(id) != 1) throw new Exception("Game ID incorrect! " + id);
			GameEntity gEntity = new GameEntity(Integer.parseInt(id), new HashSet<>());
			state.getCurrentGame().getData().add(gEntity);
			Node node = new Node(GameEntity.class, gEntity, indentLevel, state.getNode());
			state.setNode(node);
			return;
		}

		match = Regexes.ActionCreategamePlayerRegex.matcher(data);
		if (match.matches()) {
			String id = match.group(1);
			String playerId = match.group(2);
			String accountHi = match.group(3);
			String accountLo = match.group(4);
			PlayerEntity pEntity = PlayerEntity.builder().accountHi(accountHi).accountLo(accountLo)
					.playerId(Integer.parseInt(playerId)).build();
			pEntity.setTags(new HashSet<>());
			pEntity.setId(Integer.parseInt(id));
			state.updateCurrentNode(Game.class);
			state.getCurrentGame().getData().add(pEntity);
			Node node = new Node(PlayerEntity.class, pEntity, indentLevel, state.getNode());
			state.setNode(node);
			return;
		}

		match = Regexes.ActionStartRegex.matcher(data);
		if (match.matches()) {
			String rawEntity = match.group(1);
			String rawType = match.group(2);
			String index = match.group(3);
			String rawTarget = match.group(4);
			int entity = Helper.parseEntity(rawEntity, state);
			int target = Helper.parseEntity(rawTarget, state);
			int type = PowSubType.parseEnum(rawType);

			Action action = Action.builder().data(new ArrayList<>()).entity(entity).index(Integer.parseInt(index))
					.target(target).timestamp(timestamp).type(type).build();
			state.updateCurrentNode(Game.class, Action.class);

			if (state.getNode().getType().isAssignableFrom(Game.class))
				((Game) state.getNode().getObject()).getData().add(action);
			else if (state.getNode().getType().isAssignableFrom(Action.class))
				((Action) state.getNode().getObject()).getData().add(action);
			else
				throw new Exception("Invalid node " + state.getNode().getType());

			Node node = new Node(Action.class, action, indentLevel, state.getNode());
			state.setNode(node);
			return;
		}

		match = Regexes.ActionMetadataRegex.matcher(data);
		if (match.matches()) {
			String rawMeta = match.group(1);
			String rawData = match.group(2);
			String info = match.group(3);
			int parsedData = Helper.parseEntity(rawData, state);
			int meta = MetaDataType.parseEnum(rawMeta);

			MetaData metaData = MetaData.builder().data(parsedData).info(Integer.parseInt(info)).meta(meta)
					.metaInfo(new ArrayList<>()).build();
			state.updateCurrentNode(Action.class);
			log.debug("\tHandling metaData " + metaData + " on node " + state.getNode().getType());

			if (state.getNode().getType().isAssignableFrom(Action.class))
				((Action) state.getNode().getObject()).getData().add(metaData);
			else
				throw new Exception("Invalid node " + state.getNode().getType() + " for data " + data);

			Node node = new Node(MetaData.class, metaData, indentLevel, state.getNode());
			state.setNode(node);
			return;
		}

		match = Regexes.ActionMetaDataInfoRegex.matcher(data);
		if (match.matches()) {
			String index = match.group(1);
			String rawEntity = match.group(2);
			int entity = Helper.parseEntity(rawEntity, state);
			Info metaInfo = new Info(Integer.parseInt(index), entity);

			if (state.getNode().getType().isAssignableFrom(MetaData.class))
				((MetaData) state.getNode().getObject()).getMetaInfo().add(metaInfo);
			else
				throw new Exception("Invalid node " + state.getNode().getType());

			return;
		}

		match = Regexes.ActionShowEntityRegex.matcher(data);
		if (match.matches()) {
			String rawEntity = match.group(1);
			String cardId = match.group(2);
			int entity = Helper.parseEntity(rawEntity, state);

			ShowEntity showEntity = ShowEntity.builder().cardId(cardId).entity(entity).tags(new HashSet<>()).build();
			state.updateCurrentNode(Game.class, Action.class);

			if (state.getNode().getType().isAssignableFrom(Game.class))
				((Game) state.getNode().getObject()).getData().add(showEntity);
			else if (state.getNode().getType().isAssignableFrom(Action.class))
				((Action) state.getNode().getObject()).getData().add(showEntity);
			else
				throw new Exception("Invalid node " + state.getNode().getType());

			Node node = new Node(ShowEntity.class, showEntity, indentLevel, state.getNode());
			state.setNode(node);
			return;
		}

		match = Regexes.ActionHideEntityRegex.matcher(data);
		if (match.matches()) {
			String rawEntity = match.group(1);
			String tagName = match.group(2);
			String value = match.group(3);
			int entity = Helper.parseEntity(rawEntity, state);
			Tag zone = Helper.parseTag(tagName, value);

			HideEntity hideEntity = new HideEntity(timestamp, entity, zone.getValue());
			state.updateCurrentNode(Game.class, Action.class);

			if (state.getNode().getType().isAssignableFrom(Game.class))
				((Game) state.getNode().getObject()).getData().add(hideEntity);
			else if (state.getNode().getType().isAssignableFrom(Action.class))
				((Action) state.getNode().getObject()).getData().add(hideEntity);
			else
				throw new Exception("Invalid node " + state.getNode().getType());
			return;
		}

		match = Regexes.ActionFullEntityUpdatingRegex.matcher(data);
		if (!match.matches()) match = Regexes.ActionFullEntityCreatingRegex.matcher(data);

		if (match.matches()) {
			String rawEntity = match.group(1);
			String cardId = match.group(2);
			int entity = Helper.parseEntity(rawEntity, state);

			FullEntity fullEntity = new FullEntity(cardId, entity, new HashSet<>());
			state.updateCurrentNode(Game.class, Action.class);

			if (state.getNode().getType().isAssignableFrom(Game.class))
				((Game) state.getNode().getObject()).getData().add(fullEntity);
			else if (state.getNode().getType().isAssignableFrom(Action.class))
				((Action) state.getNode().getObject()).getData().add(fullEntity);
			else
				throw new Exception("Invalid node " + state.getNode().getType());

			Node node = new Node(FullEntity.class, fullEntity, indentLevel, state.getNode());
			state.setNode(node);
			return;
		}

		match = Regexes.ActionTagChangeRegex.matcher(data);
		if (match.matches()) {
			String rawEntity = match.group(1);
			String tagName = match.group(2);
			String value = match.group(3);
			Tag tag = Helper.parseTag(tagName, value);

			if (tag.getName() == GameTag.CURRENT_PLAYER.getIntValue()) updateCurrentPlayer(state, rawEntity, tag);
			int entity = Helper.parseEntity(rawEntity, state);
			if (tag.getName() == GameTag.ENTITY_ID.getIntValue())
				entity = updatePlayerEntity(state, rawEntity, tag, entity);

			TagChange tagChange = new TagChange(entity, tag.getName(), tag.getValue());
			state.updateCurrentNode(Game.class, Action.class);
			log.info("\thandling tag change " + tagChange + " on current node " + state.getNode().getType());

			if (state.getNode().getType().isAssignableFrom(Game.class))
				((Game) state.getNode().getObject()).getData().add(tagChange);
			else if (state.getNode().getType().isAssignableFrom(Action.class))
				((Action) state.getNode().getObject()).getData().add(tagChange);
			else
				throw new Exception("Invalid node " + state.getNode().getType());

			return;
		}

		match = Regexes.ActionTagRegex.matcher(data);
		if (match.matches()) {
			String tagName = match.group(1);
			String value = match.group(2);
			Tag tag = Helper.parseTag(tagName, value);

			if (tag.getName() == GameTag.CURRENT_PLAYER.getIntValue())
				state.setFirstPlayerId(((PlayerEntity) state.getNode().getObject()).getId());

			if (state.getNode().getType().isAssignableFrom(GameEntity.class))
				((GameEntity) state.getNode().getObject()).getTags().add(tag);
			else if (state.getNode().getType().isAssignableFrom(PlayerEntity.class))
				((PlayerEntity) state.getNode().getObject()).getTags().add(tag);
			else if (state.getNode().getType().isAssignableFrom(FullEntity.class))
				((FullEntity) state.getNode().getObject()).getTags().add(tag);
			else if (state.getNode().getType().isAssignableFrom(ShowEntity.class))
				((ShowEntity) state.getNode().getObject()).getTags().add(tag);
			else
				throw new Exception("Invalid node " + state.getNode().getType());
		}
	}

	private static int updatePlayerEntity(ParserState state, String rawEntity, Tag tag, int entity) {
		if (!Utils.isInteger(rawEntity) && !rawEntity.startsWith("[") && !rawEntity.equals("GameEntity")) {
			if (entity != tag.getValue()) {
				entity = tag.getValue();
				String tmpName = ((PlayerEntity) state.getCurrentGame().getData().get(1)).getName();

				((PlayerEntity) state.getCurrentGame().getData().get(1)).setName(((PlayerEntity) state.getCurrentGame()
						.getData().get(2)).getName());
				((PlayerEntity) state.getCurrentGame().getData().get(2)).setName(tmpName);

				for (Object obj : ((Game) state.getNode().getObject()).getData()) {
					TagChange tChange = obj instanceof TagChange ? (TagChange) obj : null;
					if (tChange != null) tChange.setEntity(tChange.getEntity() == 2 ? 3 : 2);
				}
			}
		}
		return entity;
	}

	private static void updateCurrentPlayer(ParserState state, String rawEntity, Tag tag) throws Exception {
		if (tag.getValue() == 0) {
			try {
				Helper.parseEntity(rawEntity, state);
			}
			catch (Exception e) {
				PlayerEntity currentPlayer = (PlayerEntity) state
						.getCurrentGame()
						.getData()
						.stream()
						.filter(x -> x instanceof PlayerEntity
								&& ((PlayerEntity) x).getId() == state.getCurrentPlayerId()).findFirst().get();
				currentPlayer.setName(rawEntity);
			}
		}
		else if (tag.getValue() == 1) {
			try {
				Helper.parseEntity(rawEntity, state);
			}
			catch (Exception e) {
				PlayerEntity currentPlayer = (PlayerEntity) state
						.getCurrentGame()
						.getData()
						.stream()
						.filter(x -> x instanceof PlayerEntity
								&& ((PlayerEntity) x).getId() != state.getCurrentPlayerId()).findFirst().get();
				currentPlayer.setName(rawEntity);
			}
			state.setCurrentPlayerId(Helper.parseEntity(rawEntity, state));
		}
	}
}
