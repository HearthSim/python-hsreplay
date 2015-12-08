package com.hearthsim.hsreplay.parser.replaydata.gameactions;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElements;

import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import com.hearthsim.hsreplay.parser.replaydata.GameData;
import com.hearthsim.hsreplay.parser.replaydata.entities.FullEntity;
import com.hearthsim.hsreplay.parser.replaydata.entities.GameEntity;
import com.hearthsim.hsreplay.parser.replaydata.entities.PlayerEntity;
import com.hearthsim.hsreplay.parser.replaydata.meta.Choices;
import com.hearthsim.hsreplay.parser.replaydata.meta.MetaData;
import com.hearthsim.hsreplay.parser.replaydata.meta.SendChoices;
import com.hearthsim.hsreplay.parser.replaydata.meta.options.Options;
import com.hearthsim.hsreplay.parser.replaydata.meta.options.SendOption;

@Getter
@Setter
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
@ToString
public class Action extends GameAction {

	@XmlAttribute(name = "index")
	private int index = -1;

	@XmlAttribute(name = "target")
	private int target;

	@XmlAttribute(name = "type")
	private int type;

	//@formatter:off
	@XmlElements({
			@XmlElement(name = "Action", type = Action.class),
			@XmlElement(name = "Choices", type = Choices.class),
			@XmlElement(name = "FullEntity", type = FullEntity.class),
			@XmlElement(name = "GameEntity", type = GameEntity.class),
			@XmlElement(name = "ShowEntity", type = ShowEntity.class),
			@XmlElement(name = "HideEntity", type = HideEntity.class),
			@XmlElement(name = "Options", type = Options.class),
			@XmlElement(name = "Player", type = PlayerEntity.class),
			@XmlElement(name = "SendChoices", type = SendChoices.class),
			@XmlElement(name = "SendOption", type = SendOption.class),
			@XmlElement(name = "TagChange", type = TagChange.class),
			@XmlElement(name = "MetaData", type = MetaData.class),
			@XmlElement(name = "ChosenEntities", type = ChosenEntities.class)
	})
	//@formatter:on
	private List<GameData> data = new ArrayList<>();

	@Builder
	public Action(int index, int target, int type, List<GameData> data, int entity, String timestamp) {
		super();
		this.index = index;
		this.target = target;
		this.type = type;
		this.data = data;
		this.entity = entity;
		this.timestamp = timestamp;
	}

}
