import copy
from dataclasses import dataclass

from src.tournament.pairing.pairer import Pairer
from src.tournament.player import Player
from src.tournament.round import Round, GameResult, Pairs
from src.tournament.round_stats import RoundStats
from src.tournament.scoring.points_scorer import PointsScorer
from src.tournament.scoring.scorer import Scorer, Score


class RoundNotCompletedError(Exception):
    pass


@dataclass
class TournamentSettings:
    elo_k_value: float = 32
    scorer: Scorer = PointsScorer()


class Tournament:
    def __init__(self, players: tuple[Player, ...], settings: TournamentSettings | None = None):
        self._players = players
        self._rounds: list[Round] = []
        self.settings = settings if settings is not None else TournamentSettings()

        self.__stats_by_round_cache: list[RoundStats] = []

    def __str__(self):
        return f'<Tournament with {len(self._players)} players and {len(self._rounds)} rounds>'

    __repr__ = __str__

    @property
    def players(self):
        return self._players

    @property
    def stats(self):
        return self.get_stats(-1)

    def get_round(self, round_no: int = -1) -> Round:
        return copy.deepcopy(self._rounds[round_no])

    def get_stats(self, round_no: int = -1) -> RoundStats:
        if len(self._rounds) == 0:
            return self.__create_empty_stats_object()

        self.__calculate_stats_up_to_round(round_no % len(self._rounds))
        return self.__stats_by_round_cache[round_no]

    def __calculate_stats_up_to_round(self, max_round: int):
        stats, next_round = self.__create_empty_stats_object(), 0  # TODO: use data from cache
        self.__stats_by_round_cache = []

        while next_round <= max_round and next_round < len(self._rounds):
            stats.add_round(self._rounds[next_round])
            self.__stats_by_round_cache.append(stats.deepcopy())
            next_round += 1

    def __create_empty_stats_object(self) -> RoundStats:
        ratings = tuple(player.rating for player in self._players)
        return RoundStats(len(self._players), ratings, self.settings.elo_k_value)

    def next_round(self, pairs_or_pairer: Pairs | Pairer):
        if isinstance(pairs_or_pairer, Pairer):
            self._next_round_from_pairer(pairs_or_pairer)
        else:
            self._next_round_from_pairs(pairs_or_pairer)

    def _next_round_from_pairs(self, pairs: tuple[tuple[int, int], ...]):
        self.assert_round_completed()

        round_ = Round(len(self._players), pairs)
        self._rounds.append(round_)
        self.__clear_stats_by_round_cache()

    def _next_round_from_pairer(self, pairer: Pairer):
        self.assert_round_completed()

        pairs = pairer.pair(tuple(range(len(self._players))), self.stats, self.get_scores())
        self._next_round_from_pairs(pairs)

    def assert_round_completed(self):
        if len(self._rounds) > 0 and not self._rounds[-1].is_completed():
            raise RoundNotCompletedError

    def remove_last_round(self):
        if len(self._rounds) == 0:
            return

        self._rounds.pop()
        self.__clear_stats_by_round_cache()

    def get_round_count(self) -> int:
        return len(self._rounds)

    def set_result(self, table: int, result: GameResult | None):
        self._rounds[-1].set_result(table, result)
        self.__clear_stats_by_round_cache()

    def __clear_stats_by_round_cache(self):
        self.__stats_by_round_cache = []

    def get_scores(self) -> tuple[Score, ...]:
        return self.settings.scorer.calculate_scores(len(self._players), self._rounds, self.stats)

    def get_id_scoreboard(self) -> tuple[tuple[int, int, Score], ...]:
        scoreboard = self.settings.scorer.create_scoreboard(len(self._players), self._rounds, self.stats)
        return tuple((place, player_id, score) for place, player_id, score in scoreboard)

    def get_player_scoreboard(self) -> tuple[tuple[int, Player, Score], ...]:
        return tuple((place, self._players[player_id], score) for place, player_id, score in self.get_id_scoreboard())
