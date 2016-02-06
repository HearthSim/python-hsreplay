package info.hearthsim.hsreplay.parser;

public class Utils {
	public static boolean isInteger(String s) {
		try {
			Integer.parseInt(s);
		}
		catch (NumberFormatException e) {
			return false;
		}
		catch (NullPointerException e) {
			return false;
		}
		// only got here if we didn't return false
		return true;
	}
}
