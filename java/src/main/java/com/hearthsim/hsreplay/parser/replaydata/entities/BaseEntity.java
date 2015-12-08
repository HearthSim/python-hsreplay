package com.hearthsim.hsreplay.parser.replaydata.entities;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;

import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import com.hearthsim.hsreplay.parser.replaydata.GameData;
import com.hearthsim.hsreplay.parser.replaydata.gameactions.Tag;

@Getter
@Setter
@EqualsAndHashCode(of = { "id", "tags" }, callSuper = false)
@AllArgsConstructor
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
public abstract class BaseEntity extends GameData {

	@XmlAttribute(name = "id")
	protected int id;

	@XmlElement(name = "Tag")
	protected List<Tag> tags = new ArrayList<>();
}