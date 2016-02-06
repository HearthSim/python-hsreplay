package info.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum OptionType {

	//@formatter:off
	PASS(1),
    END_TURN(2),
    POWER(3);
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return OptionType.valueOf(tag).getIntValue();
	}
}