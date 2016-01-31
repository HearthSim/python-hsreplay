package info.hearthsim.hsreplay.bugs.forgottentorch;

import info.hearthsim.hsreplay.AbstractTestCase;

import org.junit.Test;

public class ForgottenTorchTest extends AbstractTestCase {

	@Test
	public void test() throws Exception {
		inputLogFile = "forgottentorch.txt";
		inputXmlFile = "forgottentorch.xml";

		xmlConversionTest();
	}
}
