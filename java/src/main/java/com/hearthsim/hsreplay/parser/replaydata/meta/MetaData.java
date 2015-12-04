package com.hearthsim.hsreplay.parser.replaydata.meta;

import java.util.ArrayList;
import java.util.List;

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
public class MetaData extends GameData {

	@XmlAttribute(name = "data")
	private int data;

	@XmlAttribute(name = "info")
	private int info;

	@XmlAttribute(name = "meta")
	private int meta;

	@XmlElement(name = "Info")
	private List<Info> metaInfo = new ArrayList<>();
}
