from typing import List
from src.objects.player import Player
from src.objects.round import Round, Result


class Tournament:
    def __init__(self, players, algorithm):
        self.players: List[Player] = players
        self.rounds: List[Round] = []
        self.algorithm = algorithm

    def set_result(self, game_id, result: Result):
        self.rounds[-1].set_result(game_id, result)

    def start_round(self):
        pass

    def finish_round(self):
        pass

    def get_ranking(self):
        pass
