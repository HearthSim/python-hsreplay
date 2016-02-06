package info.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum CardClass {

	//@formatter:off
	INVALID(0),
    DEATHKNIGHT(1),
    DRUID(2),
    HUNTER(3),
    MAGE(4),
    PALADIN(5),
    PRIEST(6),
    ROGUE(7),
    SHAMAN(8),
    WARLOCK(9),
    WARRIOR(10),
    DREAM(11),
    COUNT(12),

    // alias
    NEUTRAL(INVALID.getIntValue());
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return CardClass.valueOf(tag).getIntValue();
	}

}
