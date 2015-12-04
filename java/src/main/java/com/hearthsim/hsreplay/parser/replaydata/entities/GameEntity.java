package com.hearthsim.hsreplay.parser.replaydata.entities;

import java.util.Set;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlRootElement;

import lombok.NoArgsConstructor;
import lombok.ToString;

import com.hearthsim.hsreplay.parser.replaydata.gameactions.Tag;

@XmlRootElement(name = "GameEntity")
@NoArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
public class GameEntity extends BaseEntity {

	public GameEntity(int id, Set<Tag> tags) {
		super(id, tags);
	}

}
