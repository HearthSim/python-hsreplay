package info.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum Mulligan {

	//@formatter:off
	INVALID(0),
    INPUT(1),
    DEALING(2),
    WAITING(3),
    DONE(4);
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return Mulligan.valueOf(tag).getIntValue();
	}
}