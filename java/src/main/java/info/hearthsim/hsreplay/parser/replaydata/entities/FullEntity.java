package info.hearthsim.hsreplay.parser.replaydata.entities;

import java.util.List;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlRootElement;

import org.apache.commons.lang.StringUtils;

import info.hearthsim.hsreplay.parser.replaydata.gameactions.Tag;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import lombok.ToString;

@XmlRootElement(name = "FullEntity")
@AllArgsConstructor
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
public class FullEntity extends BaseEntity {

	@XmlAttribute(name = "cardID")
	private String cardId;

	public FullEntity(String timestamp, String cardId, int entity, List<Tag> tags) {
		super(entity, tags);
		this.cardId = cardId;
		this.timestamp = timestamp;
	}

	public boolean shouldSerializeCardId() {
		return StringUtils.isNotEmpty(cardId);
	}
}
