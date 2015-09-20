#region

using System.IO;
using System.Reflection;

#endregion

namespace HearthstoneReplayTests
{
	internal class TestDataReader
	{
		public static TextReader GetInputFile(string filename)
		{
			Assembly thisAssembly = Assembly.GetExecutingAssembly();
			return new StreamReader(thisAssembly.GetManifestResourceStream("HearthstoneReplayTests.TestData." + filename));
		}
	}
}