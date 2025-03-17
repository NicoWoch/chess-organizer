import itertools
import math
from typing import Iterable, Any

from src.algorithms.bracket_pairer import BracketPairer, PairsSet
from src.algorithms.constants import Points, Result
from src.algorithms.graph import Graph
from src.algorithms.tournament import Pairs


def get_optimal_swiss_rounds(no_players: int) -> int:
    return math.ceil(math.log2(no_players))


class SwissPairer(BracketPairer):
    def get_starting_points(self) -> Points:
        return Points(2)

    def calculate_small_points(self, points: list[Points], till_round: int = None) -> Iterable[Points]:
        results_points: list[dict[Result, int]] = [{} for _ in self.tournament.players]

        for game in self.tournament.iterate_over_all_games(till_round):
            results_points[game.white][game.result] += points[game.black].big
            results_points[game.black][game.result.opposite()] += points[game.white].big

        for player, results in enumerate(results_points):
            points[player].set_small_points((
                results[Result.White] * 3 + results[Result.Draw],
                results[Result.Black]
            ))

        return points

    def __pair_first_round(self) -> Pairs:
        pairs_count = self.tournament.players_count // 2
        return tuple(
            (i, i + pairs_count)
            for i in range(pairs_count)
        )

    def _pairs_order_key(self, pair: tuple[int, int]) -> Any:
        white_player, black_player = self.tournament.players[pair[0]], self.tournament.players[pair[1]]
        white_points, black_points = self.points[pair[0]], self.points[pair[1]]

        desc_key = (
            max(white_points.big, black_points.big),
            white_points.big + black_points.big,
            white_points.base_big + black_points.base_big,  # if someone was on pause put him lower
            max(white_player.rating, black_player.rating),
            white_player.rating + black_player.rating,
            str(white_player) + str(black_player),
        )
        asc_key = tuple(-val for val in desc_key)
        return asc_key

    def _prepare_for_pairing(self):
        super()._prepare_for_pairing()
        self.opponents: list[set[int]] = [set() for _ in range(self.tournament.players_count)]
        self.color_balance: list[int] = [0] * self.tournament.players_count
        self.color_repeats: list[int] = [0] * self.tournament.players_count

        for game in self.tournament.iterate_over_all_games():
            self.opponents[game.white].add(game.black)
            self.opponents[game.black].add(game.white)

            self.color_balance[game.white] += 1
            self.color_balance[game.black] -= 1

            self.color_repeats[game.white] = max(self.color_repeats[game.white], 0) + 1
            self.color_repeats[game.black] = min(self.color_repeats[game.black], 0) - 1

    def _pair_bracket(self, bracket: set[int]) -> PairsSet:
        graph = Graph()
        graph.add_nodes(bracket)

        for edge in itertools.combinations(bracket, 2):
            if self.__can_make_edge(*edge):
                graph.add_edge(edge, self.__calculate_edge_weight(*edge))

        pairs = graph.max_weight_matching()
        return {self.__get_best_pair_order(*pair) for pair in pairs}

    def __can_make_edge(self, a: int, b: int) -> bool:
        if a in self.opponents[b]:
            return False

        has_a_forced_white = self.color_balance[a] <= -2 or self.color_repeats[a] <= -2
        has_b_forced_white = self.color_balance[b] <= -2 or self.color_repeats[b] <= -2

        has_a_forced_black = self.color_balance[a] >= 2 or self.color_repeats[a] >= 2
        has_b_forced_black = self.color_balance[b] >= 2 or self.color_repeats[b] >= 2

        if has_a_forced_white and has_b_forced_white:
            return False

        if has_a_forced_black and has_b_forced_black:
            return False

        return True

    def __calculate_edge_weight(self, a: int, b: int) -> tuple[int, ...]:
        color_connection = (abs(self.color_balance[a] - self.color_balance[b]) +
                            abs(self.color_repeats[a] - self.color_repeats[b])) ** 2

        return (
            int(a in self.has_paused) + int(b in self.has_paused),
            max(self.points[a].big, self.points[b].big),
            self.points[a].big + self.points[b].big,
            color_connection,
            self.tournament.players_count - abs(a - b) - 1,
        )

    def __get_best_pair_order(self, a: int, b: int) -> tuple[int, int]:
        for diff in (4, 3, 2, 1, 0):
            if abs(self.color_balance[a] - self.color_balance[b]) >= diff:
                return (a, b) if self.color_balance[a] < self.color_balance[b] else (b, a)

            if abs(self.color_repeats[a] - self.color_repeats[b]) >= diff:
                return (a, b) if self.color_repeats[a] < self.color_repeats[b] else (b, a)

        if a in self.has_paused or b in self.has_paused:
            return (a, b) if b in self.has_paused else (b, a)

        return (a, b) if a < b else (b, a)
