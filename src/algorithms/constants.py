import operator
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.config import Config
from src.player import Player


class Result(Enum):
    White = '1 - 0'
    Black = '0 - 1'
    Draw = '½ - ½'
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
        self.big_points: float = 0
        self.small_points: tuple[float, ...] = tuple([0] * small_points_count)

    def add_small_points(self, points: tuple[float, ...]):
        assert len(self.small_points) == len(points)
        self.small_points = tuple(map(operator.add, self.small_points, points))

    def __lt__(self, other):
        return (self.big_points, self.small_points) < (other.big_points, other.small_points)

    def __eq__(self, other):
        return self.big_points == other.big_points and self.small_points == other.small_points

    def __str__(self):
        points = [self.points_with_halfs(p) for p in (self.big_points, *self.small_points)]
        return ', '.join(points)

    @classmethod
    def points_with_halfs(cls, point: float) -> str:
        if point % 1 == 0:
            return str(int(point))

        if point % 1 == .5:
            if point == .5:
                return '½'

            return str(int(point)) + '½'

        return str(point)

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
