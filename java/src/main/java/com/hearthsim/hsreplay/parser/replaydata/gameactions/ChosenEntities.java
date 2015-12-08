package com.hearthsim.hsreplay.parser.replaydata.gameactions;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import com.hearthsim.hsreplay.parser.replaydata.GameData;
import com.hearthsim.hsreplay.parser.replaydata.meta.Choice;

@Getter
@Setter
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
@ToString
public class ChosenEntities extends GameData {

	@XmlAttribute(name = "entity")
	private int entity;

	@XmlAttribute(name = "playerID")
	private int playerId;

	@XmlAttribute(name = "count")
	private int count;

	@XmlElement(name = "Choice")
	private List<Choice> choices = new ArrayList<>();

	public ChosenEntities(String timestamp, int entity, int playerId, int count, List<Choice> choices) {
		super(timestamp);
		this.entity = entity;
		this.playerId = playerId;
		this.count = count;
		this.choices = choices;
		this.timestamp = timestamp;
	}

}
