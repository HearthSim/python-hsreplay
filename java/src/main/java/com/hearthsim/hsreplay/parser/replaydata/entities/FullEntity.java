package com.hearthsim.hsreplay.parser.replaydata.entities;

import java.util.HashSet;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlRootElement;

import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import lombok.ToString;

import org.apache.commons.lang.StringUtils;

import com.hearthsim.hsreplay.parser.replaydata.gameactions.Tag;

@XmlRootElement(name = "FullEntity")
@AllArgsConstructor
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
public class FullEntity extends BaseEntity {

	@XmlAttribute(name = "cardID")
	private String cardId;

	public FullEntity(String cardId, int entity, HashSet<Tag> tags) {
		super(entity, tags);
		this.cardId = cardId;
	}

	public boolean shouldSerializeCardId() {
		return StringUtils.isNotEmpty(cardId);
	}
}
