package com.hearthsim.hsreplay.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum CardType {

	//@formatter:off
	 INVALID(0),
     GAME(1),
     PLAYER(2),
     HERO(3),
     MINION(4),
     SPELL(5),
     ENCHANTMENT(6),
     WEAPON(7),
     ITEM(8),
     TOKEN(9),
     HERO_POWER(10),

     // Renamed
     ABILITY(SPELL.getIntValue());
	//@formatter:on

	private int intValue;

	public static int parseEnum(String tag) {
		try {
			int value = Integer.parseInt(tag);
			return value;
		}
		catch (Exception e) {
		}

		return CardType.valueOf(tag).getIntValue();
	}

}
