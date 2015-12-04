package com.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum Faction {

	//@formatter:off
	INVALID(0),
    HORDE(1),
    ALLIANCE(2),
    NEUTRAL(3);
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return Faction.valueOf(tag).getIntValue();
	}
}
