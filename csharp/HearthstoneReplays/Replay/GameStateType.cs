namespace HearthstoneReplays.Replay
{
	public enum GameStateType
	{
		UNKNOWN,
		ATTACK,
		JOUST,
		POWER,
		TRIGGER,
		DEATHS,
		PLAY,
		FATIGUE
	}

	public enum GameStateSubType
	{
		DRAW
	}

	public enum MetaDataType
	{
		TARGET,
		DAMAGE,
		HEALING,
		JOUST
	}
}