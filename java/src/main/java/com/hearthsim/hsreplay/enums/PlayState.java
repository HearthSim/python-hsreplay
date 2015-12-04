package com.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum PlayState {

	//@formatter:off
	 INVALID(0),
     PLAYING(1),
     WINNING(2),
     LOSING(3),
     WON(4),
     LOST(5),
     TIED(6),
     DISCONNECTED(7),
     CONCEDED(8),

     // Renamed in 10833),
     QUIT(CONCEDED.getIntValue());
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return PlayState.valueOf(tag).getIntValue();
	}
}