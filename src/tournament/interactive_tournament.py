from enum import Enum
from typing import Any, Callable

from src.serializer import CopyFieldsSerializer, Serializer, BasicSerializableType, DefaultDecoder
from src.tournament.player import Player
from src.tournament.round import Round
from src.tournament.round_stats import RoundStats
from src.tournament.tournament import Tournament, Pairer


class TournamentState(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2


class InteractiveException(Exception):
    pass


class InteractiveTournament:
    def __init__(self, on_change: Callable[[], Any] = (lambda: None),
                 update_ratings: Callable[[dict[Player, float]], Any] = (lambda: None)):
        self._players: tuple[Player, ...] = ()
        self._tournament: Tournament | None = None
        self._state = TournamentState.NOT_STARTED
        self._on_change = on_change

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

    def _assert_state(self, state: TournamentState, msg: str):
        if self._state != state:
            raise InteractiveException(msg)

    def _assert_not_state(self, state: TournamentState, msg: str):
        if self._state == state:
            raise InteractiveException(msg)

    def is_started(self) -> bool:
        return self._state == TournamentState.RUNNING

    def is_finished(self) -> bool:
        return self._state == TournamentState.FINISHED

    @staticmethod
    def _players_starting_order_key(player: Player) -> Any:
        return player.name

    def add_player(self, player: Player):
        self._assert_state(TournamentState.NOT_STARTED, 'Adding players after the tournament has started is forbidden')
        self._on_change()

        self._players = tuple(sorted(self._players + (player,), key=self._players_starting_order_key))

    def remove_player(self, player: Player):
        self._assert_state(TournamentState.NOT_STARTED,
                           'Removing players after the tournament has started is forbidden')
        self._on_change()

        self._players = tuple(sorted((p for p in self._players if p != player), key=self._players_starting_order_key))

    @property
    def players(self) -> tuple[Player, ...]:
        return self._players

    def next_round(self, *, pairer: Pairer = None, pairs: tuple[tuple[int, int], ...] = None):
        if pairer is not None and pairs is not None:
            raise ValueError('You can only specify pairs or a pairer but not both')

        if pairer is None and pairs is None:
            raise ValueError('You have to specify pairs or a pairer')

        self._assert_not_state(TournamentState.FINISHED, 'Adding rounds to a finished tournament is forbidden')
        self._on_change()

        if self._state == TournamentState.NOT_STARTED:
            if len(self._players) == 0:
                raise InteractiveException('There are no players to start the tournament')

            self._tournament = Tournament(self._players)
            self._state = TournamentState.RUNNING

        if pairs is None:
            pairs = pairer.pair(set(range(len(self._players))), self._tournament.stats)

        self._tournament.next_round(Round(len(self._players), pairs))

    def remove_last_round(self):
        self._assert_not_state(TournamentState.NOT_STARTED, 'There are no rounds to remove')
        self._assert_not_state(TournamentState.FINISHED, 'Removing rounds from a finished tournament is forbidden')
        self._on_change()

        if self._tournament.get_round_count() == 1:
            self._tournament = None
            self._state = TournamentState.NOT_STARTED
            return

        self._tournament.remove_last_round()

    def get_round(self, round_no: int = -1) -> Round:
        self._assert_not_state(TournamentState.NOT_STARTED, 'Tournament has not started yet to get round')
        return self._tournament.get_round(round_no)

    def get_round_stats(self, round_no: int = -1) -> RoundStats:
        self._assert_not_state(TournamentState.NOT_STARTED, 'Tournament has not started yet to get round stats')
        return self._tournament.get_round_stats(round_no)

    @property
    def stats(self) -> RoundStats:
        self._assert_not_state(TournamentState.NOT_STARTED, 'Tournament has not started yet to get stats')
        return self._tournament.stats

    def set_result(self, table: int, result: tuple[float, float] | None):
        self._assert_state(TournamentState.RUNNING, 'Tournament has to be running to set result on a table')
        self._on_change()

        if result is None:
            self._tournament.remove_result(table)
        else:
            self._tournament.set_result(table, *result)

    def finish(self):
        self._assert_state(TournamentState.RUNNING, 'Tournament has to be running to finish it')
        self._on_change()

        self._state = TournamentState.FINISHED

        # TODO: apply rating change to players in database


class InteractiveTournamentSerializer(CopyFieldsSerializer):
    def __init__(self):
        super().__init__(InteractiveTournament, (
            '_players',
            '_tournament',
            '_state',
        ))


class TournamentStateSerializer(Serializer):
    def can_serialize(self) -> type | tuple[type, ...]:
        return TournamentState

    def encode(self, obj: Any) -> BasicSerializableType:
        return obj.value

    def decode(self, data: BasicSerializableType, default: DefaultDecoder) -> Any:
        return TournamentState(data)
