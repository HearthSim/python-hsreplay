package com.hearthsim.hsreplay.parser.replaydata.meta;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import com.hearthsim.hsreplay.parser.replaydata.GameData;

@Getter
@Setter
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
public class SendChoices extends GameData {

	@XmlAttribute(name = "entity")
	private int entity;

	@XmlAttribute(name = "type")
	private int type;

	@XmlElement(name = "Choice")
	private List<Choice> choices = new ArrayList<>();

	public SendChoices(String timestamp, List<Choice> choices, int entity, int type) {
		super(timestamp);
		this.choices = choices;
		this.entity = entity;
		this.type = type;
	}

}
