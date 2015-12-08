package info.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum Step {

	//@formatter:off
	 INVALID(0),
     BEGIN_FIRST(1),
     BEGIN_SHUFFLE(2),
     BEGIN_DRAW(3),
     BEGIN_MULLIGAN(4),
     MAIN_BEGIN(5),
     MAIN_READY(6),
     MAIN_RESOURCE(7),
     MAIN_DRAW(8),
     MAIN_START(9),
     MAIN_ACTION(10),
     MAIN_COMBAT(11),
     MAIN_END(12),
     MAIN_NEXT(13),
     FINAL_WRAPUP(14),
     FINAL_GAMEOVER(15),
     MAIN_CLEANUP(16),
     MAIN_START_TRIGGERS(17);
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return Step.valueOf(tag).getIntValue();
	}
}
