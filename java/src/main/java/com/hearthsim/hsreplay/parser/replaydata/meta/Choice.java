package com.hearthsim.hsreplay.parser.replaydata.meta;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlRootElement;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import com.hearthsim.hsreplay.parser.replaydata.GameData;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@XmlRootElement(name = "Choice")
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
public class Choice extends GameData {

	@XmlAttribute(name = "entity")
	private int entity;

	@XmlAttribute(name = "index")
	private int index;

}
