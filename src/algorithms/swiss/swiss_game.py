from typing import List
from src.player import Player
from src.algorithms.swiss.swiss_round import SwissRound, Result


class SwissGame:
    def __init__(self, players, algorithm):
        self.players: List[Player] = players
        self.rounds: List[SwissRound] = []
        self.algorithm = algorithm

        self.algorithm.init_players(self.players)

    def set_result(self, game_id, result: Result):
        self.rounds[-1].set_result(game_id, result)

    def start_round(self):
        pairs = self.algorithm.pair_players(self.rounds)
        self.rounds.append(SwissRound(pairs, self.algorithm))

    def finish_round(self):
        self.rounds[-1].end_round()

    def get_results(self):
        return self.algorithm.get_results(self.rounds)

    def update_rankings(self):
        self.algorithm.update_rankings(self.players, self.rounds)
