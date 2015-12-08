package info.hearthsim.hsreplay.parser.replaydata.meta.options;

import info.hearthsim.hsreplay.parser.replaydata.GameData;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
@ToString
public abstract class OptionItem extends GameData {

	@XmlAttribute(name = "index")
	protected int index;

	@XmlAttribute(name = "entity")
	protected int entity;
}
