package info.hearthsim.hsreplay.parser.replaydata.gameactions;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;

import info.hearthsim.hsreplay.parser.replaydata.GameData;
import lombok.AllArgsConstructor;
import lombok.Builder;
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
public class ShowEntity extends GameData {

	@XmlAttribute(name = "cardID")
	private String cardId;

	@XmlAttribute(name = "entity")
	private int entity;

	@XmlElement(name = "Tag")
	private List<Tag> tags = new ArrayList<>();

	@Builder
	public ShowEntity(String timestamp, String cardId, int entity, List<Tag> tags) {
		super(timestamp);
		this.cardId = cardId;
		this.entity = entity;
		this.tags = tags;
		this.timestamp = timestamp;
	}

}
