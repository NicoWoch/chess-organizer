import itertools
import math

import networkx as nx

from src.algorithms.constants import Points, Result, Game
from src.algorithms.tournament import Tournament, Pairing
from src.config import Config

Pair = tuple[int, int]


def get_optimal_swiss_rounds(no_players: int) -> int:
    return math.ceil(math.log2(no_players))


def get_maximum_swiss_rounds(no_players: int) -> int:
    return no_players - 1 if no_players % 2 == 0 else no_players


class SwissTournament(Tournament):
    _floaters = None
    _color_balance = None
    _starting_numbers = None

    def _get_default_points(self) -> Points:
        return Points(2)

    def _pair_round(self, round_no: int) -> Pairing:
        if round_no == 1:
            return self.__pair_first_round()

        return self.__pair_full_round()

    def __pair_first_round(self) -> Pairing:
        players_by_rating = sorted(self.players, key=lambda x: x.rating, reverse=True)

        self._starting_numbers = [players_by_rating.index(p) for p in self._players]

        if len(players_by_rating) % 2 == 1:
            pause = [players_by_rating[-1]]
            del players_by_rating[-1]
        else:
            pause = []

        half_players_count = len(players_by_rating) // 2
        pairs = []
        for i in range(half_players_count):
            pairs.append(Game(
                players_by_rating[i],
                players_by_rating[i + half_players_count],
                Result.Playing
            ))

        return pairs, pause

    def __pair_full_round(self) -> Pairing:
        self.__update_color_balance_and_floaters()

        player_brackets = self.__make_pairing_brackets()
        brackets = []
        downfloat = set()
        for i, bracket in enumerate(player_brackets):
            paired, downfloat = self.__pair_bracket(bracket | downfloat, is_last_bracket=i == len(player_brackets) - 1)
            brackets.append(paired)

        while len(brackets) > 1:
            if len(downfloat) == 0:
                break
            elif len(downfloat) == 1 and not self.__has_paused(list(downfloat)[0]):
                break

            unpaired = self.__break_bracket(brackets[-1]) | self.__break_bracket(brackets[-2]) | downfloat
            del brackets[-2:]

            paired, downfloat = self.__pair_bracket(unpaired, is_last_bracket=True)
            brackets.append(paired)

        pairs = self.__choose_preferable_colors({pair for pairs in brackets for pair in pairs})
        sorted_pairs = self.__sort_pairs(pairs)
        games = self.__change_pairs_to_games_list(sorted_pairs)

        return games, [self._players[player_id] for player_id in downfloat]

    def __update_color_balance_and_floaters(self):
        if self._floaters is None:
            self._floaters = [0] * len(self._players)
            self._color_balance = [0] * len(self._players)

        for game in self.last_round:
            white_id, black_id = self._players.index(game.white), self._players.index(game.black)

            self._color_balance[white_id] += 1
            self._color_balance[black_id] -= 1

            self._floaters[white_id] = max(0, self._floaters[white_id]) + 1
            self._floaters[black_id] = min(0, self._floaters[black_id]) - 1

    def __make_pairing_brackets(self) -> list[set[int]]:
        points_sorted = sorted(enumerate(self._points), key=lambda p: p[1].big_points, reverse=True)

        brackets = []
        last_points = None
        for i, points in points_sorted:
            if points.big_points == last_points:
                brackets[-1].add(i)
            else:
                brackets.append({i})
                last_points = points.big_points

        return brackets

    def __pair_bracket(self, player_ids: set[int], *, is_last_bracket: bool) -> tuple[set[Pair], set[int]]:
        graph = self.__make_pairings_graph(player_ids, is_last_bracket=is_last_bracket)
        raw_pairs = nx.max_weight_matching(graph)
        unpaired = set(graph.nodes) - {node for pair in raw_pairs for node in pair}
        return raw_pairs, unpaired

    def __make_pairings_graph(self, player_ids: set[int], *, is_last_bracket: bool) -> nx.Graph:
        graph = nx.Graph()
        graph.add_nodes_from(player_ids)

        for i in player_ids:
            all_ids = player_ids - {i}
            for result, opps in self.get_opponents(i).items():
                all_ids.difference_update(opps)

            for j in all_ids:
                self.__make_edge(graph, i, j, is_last_bracket)

        return graph

    def __make_edge(self, graph: nx.Graph, player_id: int, opponent_id: int, is_last_bracket: bool):
        if self._floaters[player_id] == self._floaters[opponent_id] in (-2, 2):
            return  # Cannot make edge due to force floater +3 or -3

        if self._color_balance[player_id] == self._color_balance[opponent_id] in (-2, 2):
            return  # Cannot make edge due to force color balance -3 or 3

        graph.add_edge(player_id, opponent_id, weight=self.__calculate_weight(player_id, opponent_id, is_last_bracket))

    def __calculate_weight(self, player_id: int, opponent_id: int, is_last_bracket: bool) -> float:
        is_pause = self.__has_paused(player_id) or self.__has_paused(opponent_id)
        max_points_achievable = self.round_count * Config.WIN_POINTS

        weights_with_its_maxes = [
            (is_pause and is_last_bracket, 1),
            (
                self.get_points(player_id).big_points + self.get_points(opponent_id).big_points,
                max_points_achievable * 2
            ),
            self.__calc_preferable_color_weight(player_id, opponent_id),
            self.__calc_starting_numbers_weight(player_id, opponent_id),
            self.__calc_nearest_rating_weight(player_id, opponent_id),
        ]

        assert all(0 <= weight <= max_ for weight, max_ in weights_with_its_maxes), weights_with_its_maxes

        weights = [weight / max_ for weight, max_ in weights_with_its_maxes]
        weight = sum(weight * 100 ** i for i, weight in enumerate(reversed(weights)))

        return weight

    def __calc_preferable_color_weight(self, player_id: int, opponent_id: int) -> tuple[float, float]:
        player_pc, opponent_pc = self.__get_preferable_color(player_id), self.__get_preferable_color(opponent_id)

        if player_pc == 0 or opponent_pc == 0:
            return .5, 1

        if player_pc != opponent_pc:
            return 1, 1

        return 0, 1

    def __get_preferable_color(self, player_id: int) -> int:
        if self._color_balance[player_id] > 0:
            return -1
        elif self._color_balance[player_id] < 0:
            return 1
        elif self._floaters[player_id] > 0:
            return -1
        elif self._floaters[player_id] < 0:
            return 1

        return 0

    def __calc_starting_numbers_weight(self, player_id: int, opponent_id: int) -> tuple[float, float]:
        max_two_sn_sum = len(self._starting_numbers) * 2 - 1
        weight = max_two_sn_sum - self._starting_numbers[player_id] - self._starting_numbers[opponent_id]

        return weight, max_two_sn_sum

    def __calc_nearest_rating_weight(self, player_id: int, opponent_id: int) -> tuple[float, float]:
        max_starting_numbers_diff = len(self._starting_numbers)
        starting_number_diff = abs(self._starting_numbers[player_id] - self._starting_numbers[opponent_id])

        return max_starting_numbers_diff ** 2 - starting_number_diff ** 2, max_starting_numbers_diff ** 2

    def __has_paused(self, player_id: int) -> bool:
        return any(self._players[player_id] in pauses for pauses in self._pause)

    @classmethod
    def __break_bracket(cls, bracket: set[tuple[int, int]]) -> set[int]:
        return {i for pair in bracket for i in pair}

    def __choose_preferable_colors(self, pairs: set[Pair]) -> set[Pair]:
        return {self.__get_preferable_pair_colors(pair) for pair in pairs}

    def __get_preferable_pair_colors(self, pair: Pair) -> Pair:
        player_id, opp_id = pair
        reversed_pair = (opp_id, player_id)

        if self._color_balance[player_id] != self._color_balance[opp_id]:
            return pair if self._color_balance[player_id] < self._color_balance[opp_id] else reversed_pair

        if self._floaters[player_id] != self._floaters[opp_id]:
            return pair if self._floaters[player_id] < self._floaters[opp_id] else reversed_pair

        return pair if self._starting_numbers[player_id] > self._starting_numbers[opp_id] else reversed_pair

    def __sort_pairs(self, pairs: set[Pair]) -> list[Pair]:
        def sort_key(a: int, b: int):
            return (
                max(self._points[a].big_points, self._points[b].big_points),
                self._points[a].big_points + self._points[b].big_points,
                max(self._points[a].small_points, self._points[b].small_points),
                max(self._players[a].rating, self._players[b].rating),
                self._players[a].rating + self._players[b].rating,
                self._players[a].name, self._players[b].name,
            )

        return sorted(pairs, key=lambda pair: sort_key(*pair), reverse=True)

    def __change_pairs_to_games_list(self, pairs: list[Pair]) -> list[Game]:
        games = []
        for pair in pairs:
            games.append(Game(self._players[pair[0]], self._players[pair[1]], Result.Playing))

        return games

    def _update_small_points(self):
        for i, opps in enumerate(self._opponents):
            win_op_points = sum(self._points[j].big_points for j in opps[Result.White])
            draw_op_points = sum(self._points[j].big_points for j in opps[Result.Draw])
            lost_op_points = sum(self._points[j].big_points for j in opps[Result.Black])

            self._points[i].small_points = (
                win_op_points * 3 + draw_op_points,
                lost_op_points
            )
