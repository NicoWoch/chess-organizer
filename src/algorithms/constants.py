import operator
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.config import Config
from src.player import Player


class Result(Enum):
    White = '2 - 0'
    Black = '0 - 2'
    Draw = '1 - 1'
    Playing = '-'

    def opposite(self):
        if self == Result.White:
            return Result.Black
        elif self == Result.Black:
            return Result.White
        else:
            return self

    def get_points(self):
        if self == Result.White:
            return Config.WIN_POINTS
        elif self == Result.Draw:
            return Config.DRAW_POINTS
        elif self == Result.Black:
            return Config.LOSE_POINTS
        else:
            return 0


class Points:
    def __init__(self, small_points_count: int):
        self.big_points = 0
        self.small_points = tuple([0] * small_points_count)

    def add_small_points(self, points: tuple[int, ...]):
        assert len(self.small_points) == len(points)
        self.small_points = tuple(map(operator.add, self.small_points, points))

    def __lt__(self, other):
        return (self.big_points, self.small_points) < (other.big_points, other.small_points)

    def __eq__(self, other):
        return self.big_points == other.big_points and self.small_points == other.small_points

    def __str__(self):
        return ', '.join(map(str, (self.big_points, *self.small_points)))

    def __repr__(self):
        return str((self.big_points, *self.small_points))


@dataclass
class Game:
    white: Optional[Player]
    black: Optional[Player]
    result: Optional[Result]

    def __str__(self):
        return f'<Game "{self.white}" - "{self.black}" = "{self.result}">'

    __repr__ = __str__


Round = list[Game]
