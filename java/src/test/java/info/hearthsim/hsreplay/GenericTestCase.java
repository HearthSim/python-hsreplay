package info.hearthsim.hsreplay;

import org.junit.Test;

public class GenericTestCase extends AbstractTestCase {

	/**
	 * Very generic test case to check for regressions. Should develop more
	 * specific test cases as the implementation evolves
	 */
	@Test
	public void test() throws Exception {
		inputLogFile = "output_log.txt";
		inputXmlFile = "expected_xml.xml";

		super.xmlConversionTest();
	}
}
