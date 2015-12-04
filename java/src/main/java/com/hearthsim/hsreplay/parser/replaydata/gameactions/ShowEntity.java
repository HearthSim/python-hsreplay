package com.hearthsim.hsreplay.parser.replaydata.gameactions;

import java.util.HashSet;
import java.util.Set;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import com.hearthsim.hsreplay.parser.replaydata.GameData;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
public class ShowEntity extends GameData {

	@XmlAttribute(name = "cardID")
	private String cardId;

	@XmlAttribute(name = "entity")
	private int entity;

	@XmlElement(name = "Tag")
	private Set<Tag> tags = new HashSet<>();
}
