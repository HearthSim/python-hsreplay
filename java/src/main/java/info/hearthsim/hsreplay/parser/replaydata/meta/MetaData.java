package info.hearthsim.hsreplay.parser.replaydata.meta;

import info.hearthsim.hsreplay.parser.replaydata.GameData;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;

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
@XmlAccessorOrder(XmlAccessOrder.ALPHABETICAL)
@ToString
public class MetaData extends GameData {

	@XmlAttribute(name = "data")
	private int data;

	@XmlAttribute(name = "info")
	private int info;

	@XmlAttribute(name = "meta")
	private int meta;

	@XmlElement(name = "Info")
	private List<Info> metaInfo = new ArrayList<>();
}
