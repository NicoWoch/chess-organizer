import operator
from dataclasses import dataclass
from enum import Enum

from src.config import Config


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
    def __init__(self, small_points_count: int, base_big: float = 0, pause: int = 0, small: tuple[float, ...] = None):
        self.base_big = base_big
        self.pause = pause
        self.small = small if small is not None else (0.,) * small_points_count

    @property
    def big(self) -> float:
        return self.base_big + self.pause

    def add_small_points(self, points: tuple[float, ...]):
        assert len(self.small) == len(points)
        self.small = tuple(map(operator.add, self.small, points))

    def set_small_points(self, points: tuple[float, ...]):
        assert len(self.small) == len(points)
        self.small = points

    def __lt__(self, other):
        return (self.big, self.small) < (other.big, other.small)

    def __eq__(self, other):
        return self.big == other.big and self.small == other.small

    def __str__(self):
        points = [self.points_with_halfs(p) for p in (self.big, *self.small)]
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
        return str((self.big, *self.small))


@dataclass(frozen=True)
class Game:
    white: int
    black: int
    result: Result = Result.Playing

    def __str__(self):
        return f'<Game "{self.white}" - "{self.black}" = "{self.result}">'

    __repr__ = __str__
