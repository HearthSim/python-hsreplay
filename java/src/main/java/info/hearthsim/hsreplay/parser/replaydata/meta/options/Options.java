package info.hearthsim.hsreplay.parser.replaydata.meta.options;

import info.hearthsim.hsreplay.parser.replaydata.GameData;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessOrder;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorOrder;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;

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
public class Options extends GameData {

	@XmlAttribute(name = "id")
	private int id;

	@XmlElement(name = "Option")
	private List<Option> optionList = new ArrayList<>();

	public Options(String timestamp, int id, List<Option> optionList) {
		super(timestamp);
		this.id = id;
		this.optionList = optionList;
	}

}
