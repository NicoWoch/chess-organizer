class PlayerExistsError(Exception):
    def __init__(self):
        super().__init__(f'Player is already added to tournament')


class TournamentStartedError(Exception):
    def __init__(self):
        super().__init__(f'Tournament should not be started')


class TournamentNotRunningError(Exception):
    def __init__(self):
        super().__init__(f'Tournament should be running')


class TournamentEndedError(Exception):
    def __init__(self):
        super().__init__(f'Tournament should not be ended')


class RoundNotEnded(Exception):
    def __init__(self, tables_count):
        super().__init__(f'Games not ended on {tables_count} tables')
