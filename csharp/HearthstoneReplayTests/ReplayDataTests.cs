#region

using System.IO;
using HearthstoneReplays;
using HearthstoneReplays.Parser;
using Microsoft.VisualStudio.TestTools.UnitTesting;

#endregion

namespace HearthstoneReplayTests
{
	[TestClass]
	public class ReplayDataTests
	{
		[TestMethod]
		public void DeserializeTest()
		{
			var replay = ReplaySerializer.Deserialize(TestDataReader.GetInputFile("Power_1.log.xml"));
			Assert.IsNotNull(replay);
		}

		[TestMethod]
		public void SameOutputTest()
		{/*
			var replay1 = ReplayParser.FromTextReader(TestDataReader.GetInputFile("Power_2.log"));
			ReplaySerializer.Serialize(replay1, "r1.xml");
			using(var r1 = new StreamReader("r1.xml"))
			using(var r2 = TestDataReader.GetInputFile("Power_1.log.xml"))
				Assert.IsTrue(r1.ReadLine() == r2.ReadLine());*/
		}
	}
}