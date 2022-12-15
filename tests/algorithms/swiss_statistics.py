import itertools
import math
import random

import matplotlib.pyplot as plt

from src.algorithms.constants import Result
from src.algorithms.swiss_tournament import SwissTournament
from src import dummy_generator as dummy
from src.player import Player


def get_random_players(no_players: int, rng: random.Random) -> list[Player]:
    while True:
        players = dummy.get_random_players(no_players, rng=rng)

        if len(set(players)) == len(players):
            return players


def get_max_rounds(no_players: int, rng: random.Random) -> int:
    players = get_random_players(no_players, rng)
    games_count = no_players // 2

    tournament = SwissTournament('tournament')
    tournament.add_players(players)

    for round_no in itertools.count():
        tournament.next_round()

        if len(tournament.get_pause()) != no_players % 2:
            return round_no

        assert len(tournament.last_round) == games_count

        for i in range(games_count):
            tournament.set_result(i, rng.choice([Result.White, Result.Draw, Result.Black]))


def get_max_rounds_better(no_players: int, test_count: int, rng: random.Random):
    max_rounds = float('inf')
    for _ in range(test_count):
        max_rounds = min(max_rounds, get_max_rounds(no_players, rng=rng))

    return max_rounds


def main():
    players_range = list(range(5, 60, 3))
    rng = random.Random(372)

    max_rounds = []
    for i in players_range:
        print(f'Getting max range for {i} players')
        max_rounds.append(get_max_rounds_better(i, 5, rng=rng))

    plt.plot(players_range, [math.ceil(math.log2(i)) for i in players_range], color='red')
    plt.plot(players_range, [i + 1 for i in players_range], color='green')

    plt.plot(players_range, [6 for _ in players_range], color='black')
    plt.plot(players_range, [7 for _ in players_range], color='black')
    plt.plot(players_range, [8 for _ in players_range], color='black')


    plt.plot(players_range, max_rounds, color='blue')
    plt.show()
    # print(get_max_rounds_better(20, random.Random(23), 25))


if __name__ == '__main__':
    main()
