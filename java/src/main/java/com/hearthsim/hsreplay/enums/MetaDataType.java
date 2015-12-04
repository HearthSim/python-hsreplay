package com.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum MetaDataType {

	//@formatter:off
	// From HistoryMeta.Type
    TARGET(0),
    DAMAGE(1),
    HEALING(2),
    JOUST(3),

    // Renamed in 9786 from PowerHistoryMetaData.Type
    META_TARGET(TARGET.getIntValue()),
    META_DAMAGE(DAMAGE.getIntValue()),
    META_HEALING(HEALING.getIntValue());
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return MetaDataType.valueOf(tag).getIntValue();
	}

}