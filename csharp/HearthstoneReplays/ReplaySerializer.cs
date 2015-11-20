#region

using System.IO;
using System.Xml;
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
			var ns = new XmlSerializerNamespaces();
			ns.Add("", "");
			var settings = new XmlWriterSettings {CloseOutput = true, Indent = true};
			using(TextWriter writer = new StreamWriter(filePath))
			using(var xmlWriter = XmlWriter.Create(writer, settings))
			{
				xmlWriter.WriteStartDocument();
				xmlWriter.WriteDocType("hsreplay", null, string.Format(@"http://hearthsim.info/hsreplay/dtd/hsreplay-{0}.dtd", replay.Version),
				                       null);
				Serializer.Serialize(xmlWriter, replay, ns);
				xmlWriter.WriteEndDocument();
			}
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