from dataclasses import dataclass
from enum import Enum
from typing import Optional

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


@dataclass
class Game:
    white: Optional[Player]
    black: Optional[Player]
    result: Optional[Result]

    def __str__(self):
        return f'<Game "{self.white}" - "{self.black}" = "{self.result}">'

    def __repr__(self):
        return self.__str__()


Round = list[Game]
