package com.hearthsim.hsreplay.parser.replaydata.gameactions;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Setter
@Getter
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
public class Tag {

	@XmlAttribute(name = "tag")
	private int name;

	@XmlAttribute(name = "value")
	private int value;
}
