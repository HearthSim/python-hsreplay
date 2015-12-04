package com.hearthsim.hsreplay.parser.replaydata.entities;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@XmlAccessorType(XmlAccessType.FIELD)
@ToString
public class PlayerEntity extends BaseEntity {

	@XmlAttribute(name = "accountHi")
	private String accountHi;

	@XmlAttribute(name = "accountLo")
	private String accountLo;

	@XmlAttribute(name = "playerID")
	private int playerId;

	@XmlAttribute(name = "name")
	private String name;
}
