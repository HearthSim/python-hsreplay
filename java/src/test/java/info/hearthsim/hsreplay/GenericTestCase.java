package info.hearthsim.hsreplay;

import static org.junit.Assert.*;

import java.util.Scanner;

import org.junit.Test;

public class GenericTestCase {

	private final ReplaySerializer parser = new ReplaySerializer();

	/**
	 * Very generic test case to check for regressions. Should develop more
	 * specific test cases as the implementation evolves
	 */
	@SuppressWarnings("resource")
	@Test
	public void test() throws Exception {

		String inputLogFile = "output_log.0.13.5.txt";

		String expectedXmlAString = new Scanner(getClass().getResourceAsStream("expected_xml.xml"), "UTF-8")
				.useDelimiter("\\A").next();
		String logFile = new Scanner(getClass().getResourceAsStream(inputLogFile), "UTF-8").useDelimiter("\\A").next();

		String xml = parser.xmlFromLogs(logFile);

		String expectedXmlOneLiner = expectedXmlAString.replaceAll("\t", "").replaceAll("\n", "").replaceAll("\r", "");
		String xmlOneLiner = xml.replaceAll("\t", "").replaceAll("\n", "").replaceAll("\r", "");
		// System.out.println(expectedXmlOneLiner);
		System.out.println(xmlOneLiner);

		assertEquals(expectedXmlOneLiner, xmlOneLiner);
	}
}
