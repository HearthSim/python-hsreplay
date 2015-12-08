package com.hearthsim.hsreplay.parser.replaydata.gameactions;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;

import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@EqualsAndHashCode(of = { "name", "value" }, callSuper = false)
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
@ToString
public class TagChange extends GameAction {

	@XmlAttribute(name = "tag")
	private int name;

	@XmlAttribute(name = "value")
	private int value;

	public TagChange(int entity, int name, int value) {
		super(entity);
		this.name = name;
		this.value = value;
	}

}
