package com.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum Zone {

	//@formatter:off
	INVALID(0),
    PLAY(1),
    DECK(2),
    HAND(3),
    GRAVEYARD(4),
    REMOVEDFROMGAME(5),
    SETASIDE(6),
    SECRET(7),

    // Not public
    DISCARD(-2);
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return Zone.valueOf(tag).getIntValue();
	}
}