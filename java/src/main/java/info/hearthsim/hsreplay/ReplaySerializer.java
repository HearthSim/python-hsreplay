package info.hearthsim.hsreplay;

import java.io.StringWriter;
import java.util.Arrays;
import java.util.List;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.Marshaller;

import info.hearthsim.hsreplay.parser.ReplayParser;
import info.hearthsim.hsreplay.parser.replaydata.HearthstoneReplay;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ReplaySerializer {

	public String xmlFromLogs(String logString) throws Exception {
		List<String> lines = Arrays.asList(logString.split(System.lineSeparator()));
		HearthstoneReplay replay = new ReplayParser().fromString(lines);
		log.debug("Converted into replay: " + replay);

		String xmlReplay = xmlFromReplay(replay);
		return xmlReplay;
	}

	public String xmlFromReplay(HearthstoneReplay replay) throws Exception {
		JAXBContext jaxbContext = JAXBContext.newInstance(HearthstoneReplay.class);
		Marshaller marshaller = jaxbContext.createMarshaller();
		// MarshallerImpl impl;
		// impl.
		marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);
		marshaller.setProperty(Marshaller.JAXB_ENCODING, "UTF-8");
		marshaller.setProperty("com.sun.xml.bind.indentString", "\t");

		StringWriter stringWriter = new StringWriter();
		marshaller.marshal(replay, stringWriter);

		return stringWriter.toString();
	}
}
