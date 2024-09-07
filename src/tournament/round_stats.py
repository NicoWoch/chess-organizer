import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Self, Iterable

from src.serializer import CopyFieldsSerializer
from src.tournament.round import Round


@dataclass(frozen=True)
class RoundStats:
    round_count: int

    played_together: defaultdict[tuple[int, int], int]
    played_as_a: defaultdict[int, int]
    played_as_b: defaultdict[int, int]
    paused: defaultdict[int, int]

    points: defaultdict[int, float]

    floaters: defaultdict[int, int]

    @classmethod
    def make_from_rounds(cls, rounds: Iterable[Round]) -> Self:
        stats = [cls.make_from_round(round_) for round_ in rounds]
        return sum(stats, cls.make_empty())

    @classmethod
    def make_empty(cls) -> Self:
        return RoundStats(0, defaultdict(int), defaultdict(int), defaultdict(int),
                          defaultdict(int), defaultdict(float), defaultdict(int))

    @classmethod
    def make_from_round(cls, round_: Round) -> Self:
        played_together: defaultdict[tuple[int, int], int] = defaultdict(int)
        played_as_a: defaultdict[int, int] = defaultdict(int)
        played_as_b: defaultdict[int, int] = defaultdict(int)
        paused: defaultdict[int, int] = defaultdict(int, {p: 1 for p in round_.pause})
        points: defaultdict[int, float] = defaultdict(float)
        floaters: defaultdict[int, int] = defaultdict(int)

        games_with_result = ((pair, result) for pair, result in zip(round_.pairs, round_.results) if result is not None)

        for (player_a, player_b), result in zip(round_.pairs, round_.results):
            played_together[(player_a, player_b)] += 1
            played_together[(player_b, player_a)] += 1

            played_as_a[player_a] += 1
            played_as_b[player_b] += 1

            floaters[player_a] = 1
            floaters[player_b] = -1

        for (player_a, player_b), (score_a, score_b) in games_with_result:
            points[player_a] += score_a
            points[player_b] += score_b

        return RoundStats(1, played_together, played_as_a, played_as_b, paused, points, floaters)

    def __add__(self, other: Self) -> Self:
        new_floaters = self.__add_dicts(self.floaters, other.floaters)

        for player in new_floaters.keys():
            floater_1, floater_2 = self.floaters[player], other.floaters[player]

            if floater_1 == 0:
                new_floaters[player] = floater_2
            elif floater_2 == 0:
                new_floaters[player] = floater_1
            elif math.copysign(1, floater_1) == math.copysign(1, floater_2):
                new_floaters[player] = floater_1 + floater_2
            else:
                new_floaters[player] = floater_2

        return RoundStats(
            self.round_count + other.round_count,
            self.__add_dicts(self.played_together, other.played_together),
            self.__add_dicts(self.played_as_a, other.played_as_a),
            self.__add_dicts(self.played_as_b, other.played_as_b),
            self.__add_dicts(self.paused, other.paused),
            self.__add_dicts(self.points, other.points),
            new_floaters
        )

    @staticmethod
    def __add_dicts(dict_a: defaultdict, dict_b: defaultdict) -> defaultdict:
        new_dict = defaultdict(dict_a.default_factory)

        for key in dict_a.keys() | dict_b.keys():
            new_dict[key] = dict_a[key] + dict_b[key]

        return new_dict


class RoundStatsSerializer(CopyFieldsSerializer):
    def __init__(self):
        super().__init__(RoundStats, (
            'round_count',
            'played_together',
            'played_as_a',
            'played_as_b',
            'paused',
            'points',
            'floaters',
        ))
