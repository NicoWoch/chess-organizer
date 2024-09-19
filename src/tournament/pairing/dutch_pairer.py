import itertools
import logging
from typing import Iterator

import networkx as nx

from src.tournament.pairing.bracket_pairer import BracketPairer
from src.tournament.pairing.pairer import ListPairs
from src.tournament.round import Pairs

logger = logging.getLogger(__name__)


class TupleWeightedGraph:
    def __init__(self):
        self.edges: list[tuple[int, int]] = []
        self.weights: list[tuple[int, ...]] = []
        self.max_tuple_values = []

    def add_edge(self, u: int, v: int, weight: tuple[int, ...]):
        self.edges.append((u, v))
        self.weights.append(weight)

        self.max_tuple_values.extend([0] * (len(weight) - len(self.max_tuple_values)))

        for i, value in enumerate(weight):
            if value < 0:
                raise ValueError(f'Weight canot be negative {weight}')

            self.max_tuple_values[i] = max(value, self.max_tuple_values[i])

    def max_weight_matching(self, *, maxcardinality=False) -> set:
        graph = nx.Graph()
        graph.add_weighted_edges_from(self.__create_weighted_edges())

        return nx.max_weight_matching(graph, maxcardinality=maxcardinality)

    def __create_weighted_edges(self) -> Iterator[tuple[int, int, int]]:
        for edge, weight in zip(self.edges, self.weights):
            yield edge[0], edge[1], self.__map_tuple_to_int(weight)

    def __map_tuple_to_int(self, tpl: tuple[int, ...]) -> int:
        code = 0

        for i, max_value in enumerate(self.max_tuple_values):
            code *= max_value + 1
            code += tpl[i] if i < len(tpl) else 0

        return code


class DutchPairer(BracketPairer):
    def _pair_first_round(self) -> Pairs:
        half = len(self.players) // 2
        return tuple((i, half + i) for i in self.players[:half])

    def _pair_bracket(self, players: set[int], downfloat: set[int], *, is_last: bool) -> ListPairs:
        players |= downfloat

        self.__downfloat = downfloat
        self.__is_last = is_last

        graph = self.__create_graph(players)
        matching = graph.max_weight_matching(maxcardinality=is_last)

        logger.debug(f'Bracket matching: {matching}')

        return list(matching)

    def __create_graph(self, players: set[int]) -> TupleWeightedGraph:
        graph = TupleWeightedGraph()

        for player_1, player_2 in itertools.permutations(players, 2):
            if player_1 >= player_2:
                continue

            if not self.__can_play_with_each_other(player_1, player_2):
                continue

            weight = self.__calculate_weight(player_1, player_2)
            graph.add_edge(player_1, player_2, weight)

        return graph

    def __can_play_with_each_other(self, player_1: int, player_2: int) -> bool:
        if self.stats.color_repetition[player_1] == self.stats.color_repetition[player_2] == -2:
            return False

        if self.stats.color_repetition[player_1] == self.stats.color_repetition[player_2] == +2:
            return False

        return self.stats.played_together[player_1][player_2] == 0

    def __calculate_weight(self, player_1: int, player_2: int) -> tuple[int, ...]:
        has_pause = self.stats.paused[player_1] > 0 or self.stats.paused[player_2] > 0

        return (
            (1 if self.__is_last and has_pause else 0),
            *self.__calc_scores_weight(player_1, player_2),
            *self.__calc_color_preference_weight(player_1, player_2),
            *self.__calc_starting_numbers_weight(player_1, player_2),
            *self.__calc_ratings_weight(player_1, player_2),
        )

    def __calc_scores_weight(self, player_1: int, player_2: int) -> tuple[int, ...]:
        return (
            # TODO
        )

    def __calc_color_preference_weight(self, player_1: int, player_2: int) -> tuple[int, ...]:
        return (
            # TODO
        )

    def __calc_starting_numbers_weight(self, player_1: int, player_2: int) -> tuple[int, ...]:
        return (
            # TODO
        )

    def __calc_ratings_weight(self, player_1: int, player_2: int) -> tuple[int, ...]:
        return (
            # TODO
        )
