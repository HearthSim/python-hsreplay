package info.hearthsim.hsreplay.bugs.palareinforce;

import info.hearthsim.hsreplay.AbstractTestCase;

import org.junit.Test;

public class TestCase extends AbstractTestCase {

	@Test
	public void test() throws Exception {
		inputLogFile = "log.txt";
		inputXmlFile = "log.xml";

		xmlConversionTest();
	}
}
