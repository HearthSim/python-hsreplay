package info.hearthsim.hsreplay.parser.replaydata.gameactions;

import info.hearthsim.hsreplay.parser.replaydata.GameData;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
@ToString
public class HideEntity extends GameData {

	@XmlAttribute(name = "entity")
	private int entity;

	@XmlAttribute(name = "zone")
	private int zone;

	public HideEntity(String timestamp, int entity, int zone) {
		super(timestamp);
		this.entity = entity;
		this.zone = zone;
	}

}
