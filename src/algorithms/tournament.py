from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, List

from src.player import Player


class Result(Enum):
    White = auto()
    Black = auto()
    Draw = auto()
    Playing = auto()


@dataclass
class Game:
    white: Player
    black: Player
    result: Result


Round = List[Game]


class Tournament(ABC):
    @abstractmethod
    def __init__(self, players: List[Player]): ...

    @abstractmethod
    def get_players(self) -> List[Player]: ...

    @abstractmethod
    def get_waiting_players(self, round_id=-1) -> List[Player]: ...

    @abstractmethod
    def get_rounds(self) -> List[Round]: ...

    def get_last_round(self) -> Round:
        return self.get_rounds()[-1]

    def has_round_ended(self) -> bool:
        return all(game.result != Result.Playing for game in self.get_last_round())

    @abstractmethod
    def get_scoreboard(self) -> List[Tuple[Player, object]]: ...

    @abstractmethod
    def set_result(self, table_id: int, result: Result): ...

    @abstractmethod
    def next_round(self): ...

    @abstractmethod
    def end_tournament(self): ...
