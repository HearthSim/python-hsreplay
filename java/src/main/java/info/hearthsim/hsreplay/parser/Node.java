package info.hearthsim.hsreplay.parser;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@ToString(of = { "type", "parent" })
public class Node {

	private Class<? extends Object> type;
	private Object object;
	private int indentLevel;
	private Node parent;
}
