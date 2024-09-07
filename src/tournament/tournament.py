import copy
from abc import ABC, abstractmethod

from src.serializer import CopyFieldsSerializer
from src.tournament.player import Player
from src.tournament.round import Round
from src.tournament.round_stats import RoundStats


class RoundNotCompletedError(Exception):
    pass


class Pairer(ABC):
    players: set[int]
    stats: RoundStats

    def pair(self, players: set[int], stats: RoundStats):
        self.players = players
        self.stats = stats

        return self.__pair()

    @abstractmethod
    def __pair(self) -> tuple[tuple[int, int], ...]: ...


class Tournament:
    def __init__(self, players: tuple[Player, ...]):
        self._players = players
        self._rounds: list[Round] = []
        self._stats_by_round: list[RoundStats] = []
        self._stats_cache = None

    def __str__(self):
        return f'<Tournament with {len(self._rounds)} rounds>'

    __repr__ = __str__

    @property
    def players(self):
        return self._players

    @property
    def stats(self):
        if self._stats_cache is None:
            self._stats_cache = sum(self._stats_by_round, RoundStats.make_empty())

        return self._stats_cache

    def get_round(self, round_no: int = -1) -> Round:
        return copy.deepcopy(self._rounds[round_no])

    def get_round_stats(self, round_no: int = -1) -> RoundStats:
        return self._stats_by_round[round_no]

    def next_round(self, round_: Round):
        if len(self._rounds) > 0 and not self._rounds[-1].is_completed():
            raise RoundNotCompletedError

        if round_.no_players != len(self._players):
            raise ValueError('Numbers of players are different')

        self._rounds.append(round_)

        self._stats_by_round.append(RoundStats.make_from_round(round_))
        self._stats_cache = None

    def remove_last_round(self):
        if len(self._rounds) == 0:
            return

        self._rounds.pop()

        self._stats_by_round.pop()
        self._stats_cache = None

    def get_round_count(self) -> int:
        return len(self._rounds)

    def set_result(self, table: int, result_a: float, result_b: float):
        self._rounds[-1].set_result(table, result_a, result_b)
        self.__update_last_round_stats()

    def remove_result(self, table: int):
        self._rounds[-1].remove_result(table)
        self.__update_last_round_stats()

    def __update_last_round_stats(self):
        self._stats_by_round[-1] = RoundStats.make_from_round(self._rounds[-1])
        self._stats_cache = None


class TournamentSerializer(CopyFieldsSerializer):
    def __init__(self):
        super().__init__(Tournament, (
            '_players',
            '_rounds',
            '_stats_by_round',
        ))
