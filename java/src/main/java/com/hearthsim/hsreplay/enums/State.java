package com.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum State {

	//@formatter:off
	 INVALID(0),
     LOADING(1),
     RUNNING(2),
     COMPLETE(3);
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return State.valueOf(tag).getIntValue();
	}
}