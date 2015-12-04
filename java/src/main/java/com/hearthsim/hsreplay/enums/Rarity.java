package com.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum Rarity {

	//@formatter:off
	INVALID(0),
    COMMON(1),
    FREE(2),
    RARE(3),
    EPIC(4),
    LEGENDARY(5);
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return Rarity.valueOf(tag).getIntValue();
	}
}
