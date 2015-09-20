#region

using System;

#endregion

namespace HearthstoneReplays.Parser
{
	public class Node
	{
		public Node(Type type, object o, int indentLevel, Node parent)
		{
			Type = type;
			Object = o;
			IndentLevel = indentLevel;
			Parent = parent;
		}

		public Type Type { get; set; }
		public object Object { get; set; }
		public int IndentLevel { get; set; }
		public Node Parent { get; set; }
	}
}