import copy
import math
from dataclasses import dataclass
from typing import Self

from src.tournament.elo_algorithm import elo_rating_change
from src.tournament.round import Round

ELO_K_VALUE = 32
PAUSE_SCORE = 1


@dataclass(init=False)
class RoundStats:
    round_count: int
    players_count: int
    ratings: list[float]
    elo_k_value: float

    played_together: list[list[int]]
    color_balance: list[int]
    paused: list[int]
    color_repetition: list[int]

    wins: list[list[int]]
    draws: list[list[int]]
    losses: list[list[int]]

    # TODO: add floaters and recent_floaters fields

    recent_rating_changes: list[float]

    def __init__(self, players_count: int, ratings: tuple[float, ...], elo_k_value: float):
        if players_count != len(ratings):
            raise ValueError("Number of ratings does not equal number of players")

        self.round_count = 0
        self.players_count = players_count
        self.ratings = list(ratings)
        self.elo_k_value = elo_k_value

        empty_array = [0 for _ in range(players_count)]
        self.played_together = [empty_array.copy() for _ in range(players_count)]
        self.color_balance = empty_array.copy()
        self.paused = empty_array.copy()
        self.color_repetition = empty_array.copy()
        self.wins = [[] for _ in range(players_count)]
        self.draws = [[] for _ in range(players_count)]
        self.losses = [[] for _ in range(players_count)]
        self.recent_rating_changes = empty_array.copy()

    def deepcopy(self) -> Self:
        return copy.deepcopy(self)

    def add_round(self, round_: Round):
        if self.players_count != round_.no_players:
            raise ValueError("Players count mismatch")

        self.round_count += 1
        self._update_played_together(round_)
        self._update_played_sides(round_)
        self._update_paused(round_)
        self._update_floaters(round_)
        self._update_wins_draws_losses(round_)
        self._update_ratings(round_, tuple(self.ratings))

    def _update_played_together(self, round_: Round):
        for player_a, player_b in round_.pairs:
            self.played_together[player_a][player_b] += 1
            self.played_together[player_b][player_a] += 1

    def _update_played_sides(self, round_: Round):
        for player_a, player_b in round_.pairs:
            self.color_balance[player_a] += 1
            self.color_balance[player_b] -= 1

    def _update_paused(self, round_: Round):
        for pause in round_.pause:
            self.paused[pause] += 1

    def _update_floaters(self, round_: Round):
        for player_a, player_b in round_.pairs:
            for player, color_mul in ((player_a, 1), (player_b, -1)):
                if self.color_repetition[player] == 0:
                    self.color_repetition[player] = color_mul
                elif math.copysign(1, self.color_repetition[player]) == math.copysign(1, color_mul):
                    self.color_repetition[player] += color_mul
                else:
                    self.color_repetition[player] = color_mul

    def _update_wins_draws_losses(self, round_: Round):
        for (player_a, player_b), result in zip(round_.pairs, round_.results):
            if result is None or not result.is_rated or result.points_a == result.points_b == 0:
                continue

            if result.points_a > result.points_b:
                self.wins[player_a].append(player_b)
                self.losses[player_b].append(player_a)
            elif result.points_a == result.points_b:
                self.draws[player_a].append(player_b)
                self.draws[player_b].append(player_a)
            else:
                self.losses[player_a].append(player_b)
                self.wins[player_b].append(player_a)

    def _update_ratings(self, round_: Round, starting_ratings: tuple[float, ...]):
        self.recent_rating_changes = [0 for _ in range(self.players_count)]

        for (player_a, player_b), result in zip(round_.pairs, round_.results):
            if result is None or not result.is_rated:
                continue

            pa, pb = result.points_a, result.points_b
            scaled_a_points = pa / (pa + pb)
            ra, rb = starting_ratings[player_a], starting_ratings[player_b]
            art, brt = elo_rating_change(ra, rb, scaled_a_points, self.elo_k_value)

            self.recent_rating_changes[player_a] = art
            self.recent_rating_changes[player_b] = brt
            self.ratings[player_a] += art
            self.ratings[player_b] += brt
