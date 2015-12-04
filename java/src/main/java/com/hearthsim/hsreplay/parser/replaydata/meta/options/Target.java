package com.hearthsim.hsreplay.parser.replaydata.meta.options;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlRootElement;

import lombok.NoArgsConstructor;
import lombok.ToString;

@XmlRootElement(name = "Target")
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
public class Target extends OptionItem {

	public Target(int entity, int index) {
		super(index, entity);
	}

}
