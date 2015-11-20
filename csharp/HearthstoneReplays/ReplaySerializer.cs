#region

using System.IO;
using System.Xml.Serialization;
using HearthstoneReplays.Parser.ReplayData;

#endregion

namespace HearthstoneReplays
{
	public static class ReplaySerializer
	{
		private static readonly XmlSerializer Serializer = new XmlSerializer(typeof(HearthstoneReplay));

		public static void Serialize(HearthstoneReplay replay, string filePath)
		{
			using(TextWriter writer = new StreamWriter(filePath))
				Serializer.Serialize(writer, replay);
		}

		public static HearthstoneReplay Deserialize(string filePath)
		{
			using(TextReader reader = new StreamReader(filePath))
				return Deserialize(reader);
		}

		public static HearthstoneReplay Deserialize(TextReader reader)
		{
			return (HearthstoneReplay)Serializer.Deserialize(reader);
		}
	}
}