package com.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum ChoiceType {

	//@formatter:off
	INVALID(0),
    MULLIGAN(1),
    GENERAL(2);
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return ChoiceType.valueOf(tag).getIntValue();
	}

}
