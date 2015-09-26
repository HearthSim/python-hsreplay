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

    public enum ActionType
    {
        UnknownZoneChangeTC,
        UnknownZoneChangeT,
        TurnStart,
        Mulligan,
        Draw,
        Play,
        PlayFromDeck,
        HandDiscard,
        DeckDiscard,
        SecretTrigger,
        PlayToHand,
        PlayToDeck,
        CreateInHand,
        CreateInPlay,
        CreateInDeck,
        Steal,
        Attack,
        Damage,
        Death,
        Victory,
        Loss,
        Tie,
        ActionStartPlay,
        ActionStartAttack,
        ActionStartDeaths,
        ActionStartFatigue,
        ActionStartJoust,
        ActionStartPower,
        ActionStartTrigger,
        ActionStartUnknown,
        ActionEndPlay,
        ActionEndAttack,
        ActionEndDeaths,
        ActionEndFatigue,
        ActionEndJoust,
        ActionEndPower,
        ActionEndTrigger,
        ActionEndUnknown
    }
}