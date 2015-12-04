package com.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum PowSubType {

	//@formatter:off
	ATTACK(1),
    JOUST(2),
    POWER(3),
    TRIGGER(5),
    DEATHS(6),
    PLAY(7),
    FATIGUE(8),

    // Removed
    SCRIPT(4),
    ACTION(99),

    // Renamed
    CONTINUOUS(2);
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return PowSubType.valueOf(tag).getIntValue();
	}
}