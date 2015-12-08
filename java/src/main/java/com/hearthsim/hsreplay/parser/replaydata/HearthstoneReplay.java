package com.hearthsim.hsreplay.parser.replaydata;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@XmlRootElement(name = "HSReplay")
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
public class HearthstoneReplay {

	@XmlAttribute(name = "build")
	private String build;

	@XmlAttribute(name = "version")
	private String version;

	@XmlElement(name = "Game")
	private List<Game> games = new ArrayList<>();
}
