from enum import Enum, auto
from typing import List, Tuple
from .player import Player


class Result(Enum):
    WIN = auto()
    DRAW = auto()
    LOST = auto()
    PLAYING = auto()


class Round:
    def __init__(self, games, algorithm):
        self.games: List[Tuple[Player, Player]] = games
        self.results: List[Result] = [Result.PLAYING] * len(self.games)
        self.algorithm = algorithm

    def set_result(self, game_id, result: Result):
        self.results[game_id] = result

    def end_round(self):
        self.algorithm.finish_round(self)
