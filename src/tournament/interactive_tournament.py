import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Iterable

from src.tournament.player import Player
from src.tournament.round import Round, Pairs, GameResult
from src.tournament.round_stats import RoundStats
from src.tournament.scoring.scorer import Score
from src.tournament.tournament import Tournament, Pairer, TournamentSettings

logger = logging.getLogger(__name__)


class TournamentState(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2


class InteractiveException(Exception):
    pass


@dataclass
class TournamentData:
    name: str = 'Tournament'
    category: str = ''
    start_timestamp: datetime | None = None
    finish_timestamp: datetime | None = None


def ratings_not_set_error(_):
    logger.error('RATINGS NOT SET ANYWHERE!')


class InteractiveTournament:
    def __init__(self, data: TournamentData = None,
                 update_ratings: Callable[[dict[Player, float]], Any] = ratings_not_set_error):
        self.data = data if data is not None else TournamentData()
        self._players: tuple[Player, ...] = ()
        self._tournament: Tournament | None = None
        self._state = TournamentState.NOT_STARTED
        self._update_ratings = update_ratings
        self._settings = TournamentSettings()

    def __str__(self):
        return '<InteractiveTournament: ' + str({
            'players': self._players,
            'tournament': self._tournament,
            'state': self._state.name,
        }) + '>'

    __repr__ = __str__

    @property
    def state(self) -> TournamentState:
        return self._state

    @property
    def round_count(self):
        if self._tournament is None:
            return 0

        return self._tournament.get_round_count()

    def get_settings(self):
        return self._settings

    def set_settings(self, value):
        self._assert_state(TournamentState.NOT_STARTED, 'Changing settings in a running tournament is not implemented')
        self._settings = value

    def _assert_state(self, state: TournamentState, msg: str):
        if self._state != state:
            raise InteractiveException(msg)

    def _assert_not_state(self, state: TournamentState, msg: str):
        if self._state == state:
            raise InteractiveException(msg)

    def is_running(self) -> bool:
        return self._state == TournamentState.RUNNING

    def is_finished(self) -> bool:
        return self._state == TournamentState.FINISHED

    @staticmethod
    def _players_starting_order_key(player: Player) -> Any:
        return -player.rating, player

    def add_player(self, player: Player):
        self._assert_state(TournamentState.NOT_STARTED, 'Adding players after the tournament has started is forbidden')

        if player in self._players:
            raise ValueError(f'Player {player} already added to tournament')

        self._players = tuple(sorted(self._players + (player,), key=self._players_starting_order_key))

    def remove_player(self, player: Player):
        self._assert_state(TournamentState.NOT_STARTED,
                           'Removing players after the tournament has started is forbidden')

        self._players = tuple(sorted((p for p in self._players if p != player), key=self._players_starting_order_key))

    @property
    def players(self) -> tuple[Player, ...]:
        return self._players

    def next_round(self, pairs_or_pairer: Pairs | Pairer):
        self._assert_not_state(TournamentState.FINISHED, 'Adding rounds to a finished tournament is forbidden')

        if self._state == TournamentState.NOT_STARTED:
            if len(self._players) == 0:
                raise InteractiveException('There are no players to start the tournament')

            self._tournament = Tournament(self._players, self._settings)
            self._state = TournamentState.RUNNING
            self.data.start_timestamp = datetime.now()

        self._tournament.next_round(pairs_or_pairer)

    def remove_last_round(self):
        self._assert_not_state(TournamentState.NOT_STARTED, 'There are no rounds to remove')
        self._assert_not_state(TournamentState.FINISHED, 'Removing rounds from a finished tournament is forbidden')

        if self._tournament.get_round_count() == 1:
            self._tournament = None
            self._state = TournamentState.NOT_STARTED
            self.data.start_timestamp = None
            return

        self._tournament.remove_last_round()

    def get_round(self, round_no: int = -1) -> Round:
        self._assert_not_state(TournamentState.NOT_STARTED, 'Tournament has not started yet to get round')
        return self._tournament.get_round(round_no)

    def get_stats(self, round_no: int = -1) -> RoundStats:
        self._assert_not_state(TournamentState.NOT_STARTED, 'Tournament has not started yet to get round stats')
        return self._tournament.get_stats(round_no)

    @property
    def stats(self) -> RoundStats:
        self._assert_not_state(TournamentState.NOT_STARTED, 'Tournament has not started yet to get stats')
        return self._tournament.stats

    def set_result(self, table: int, result: GameResult | None):
        self._assert_state(TournamentState.RUNNING, 'Tournament has to be running to set result on a table')

        self._tournament.set_result(table, result)

    def set_results_from_iterable(self, results: Iterable[tuple[int, GameResult | None]]):
        for table_id, result in results:
            self.set_result(table_id, result)

    def get_scores(self) -> tuple[Score, ...]:
        self._assert_not_state(TournamentState.NOT_STARTED, 'Tournament has not started yet to get scores')
        return self._tournament.get_scores()

    def get_id_scoreboard(self) -> tuple[tuple[int, int, Score], ...]:
        self._assert_not_state(TournamentState.NOT_STARTED, 'Tournament has not started yet to get scoreboard')
        return self._tournament.get_id_scoreboard()

    def get_player_scoreboard(self) -> tuple[tuple[int, Player, Score], ...]:
        self._assert_not_state(TournamentState.NOT_STARTED, 'Tournament has not started yet to get scoreboard')
        return self._tournament.get_player_scoreboard()

    def finish(self):
        self._assert_state(TournamentState.RUNNING, 'Tournament has to be running to finish it')
        self._tournament.assert_round_completed()

        self._state = TournamentState.FINISHED

        ratings_changes_dict: dict[Player, float] = {}

        for player, new_rating in zip(self._players, self._tournament.stats.ratings):
            ratings_changes_dict[player] = new_rating - player.rating

        self._update_ratings(ratings_changes_dict)

        self.data.finish_timestamp = datetime.now()
