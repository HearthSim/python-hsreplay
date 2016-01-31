package info.hearthsim.hsreplay;

import static org.junit.Assert.*;

import java.util.Scanner;

public abstract class AbstractTestCase {

	private final ReplaySerializer parser = new ReplaySerializer();

	protected String inputLogFile;
	protected String inputXmlFile;

	@SuppressWarnings("resource")
	protected void xmlConversionTest() throws Exception {

		System.out.println(getClass());

		String expectedXmlAString = new Scanner(getClass().getResourceAsStream(inputXmlFile), "UTF-8").useDelimiter(
				"\\A").next();
		String logFile = new Scanner(getClass().getResourceAsStream(inputLogFile), "UTF-8").useDelimiter("\\A").next();

		String xml = parser.xmlFromLogs(logFile);

		String expectedXmlOneLiner = expectedXmlAString.replaceAll("\t", "").replaceAll("\n", "").replaceAll("\r", "");
		String xmlOneLiner = xml.replaceAll("\t", "").replaceAll("\n", "").replaceAll("\r", "");
		// System.out.println(expectedXmlOneLiner);
		System.out.println(xmlOneLiner);

		assertEquals(expectedXmlOneLiner, xmlOneLiner);
	}
}
