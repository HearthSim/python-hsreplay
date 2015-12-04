package com.hearthsim.hsreplay;

import static org.junit.Assert.*;

import java.util.Scanner;

import org.junit.Test;

public class GenericTestCase {

	private final ReplaySerializer parser = new ReplaySerializer();

	@SuppressWarnings("resource")
	@Test
	public void test() throws Exception {

		String expectedXmlAString = new Scanner(getClass().getResourceAsStream("Power_2.log.xml"), "UTF-8")
				.useDelimiter("\\A").next();

		String logFile = new Scanner(getClass().getResourceAsStream("Power_2.log.txt"), "UTF-8").useDelimiter("\\A")
				.next();

		String xml = parser.xmlFromLogs(logFile);

		String expectedXmlOneLiner = expectedXmlAString.replaceAll("\t", "").replaceAll("\n", "").replaceAll("\r", "");
		String xmlOneLiner = xml.replaceAll("\t", "").replaceAll("\n", "").replaceAll("\r", "");
		System.out.println(expectedXmlOneLiner);
		System.out.println(xmlOneLiner);

		assertEquals(expectedXmlOneLiner, xmlOneLiner);
	}
}
