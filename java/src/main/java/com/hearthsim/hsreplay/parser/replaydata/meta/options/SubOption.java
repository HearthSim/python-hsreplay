package com.hearthsim.hsreplay.parser.replaydata.meta.options;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
public class SubOption extends OptionItem {

	@XmlElement(name = "Target")
	private List<Target> targets = new ArrayList<>();

	public SubOption(int entity, int index, ArrayList<Target> targets) {
		super(index, entity);
		this.targets = targets;
	}

}
