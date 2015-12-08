package com.hearthsim.hsreplay.parser.replaydata.meta.options;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElements;
import javax.xml.bind.annotation.XmlRootElement;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import com.hearthsim.hsreplay.parser.replaydata.GameData;

@Getter
@Setter
@XmlRootElement(name = "Option")
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
@ToString
public class Option extends GameData {

	@XmlAttribute(name = "index")
	private int index;

	@XmlAttribute(name = "type")
	private int type;

	@XmlAttribute(name = "entity")
	private int entity;

	//@formatter:off
	@XmlElements({
			@XmlElement(name = "SubOption", type = SubOption.class),
			@XmlElement(name = "Target", type = Target.class),
	})
	//@formatter:on
	private List<OptionItem> optionsItems = new ArrayList<>();

	public Option(int index, int type, int entity, List<OptionItem> optionsItems) {
		super();
		this.index = index;
		this.type = type;
		this.entity = entity;
		this.optionsItems = optionsItems;
	}

}
