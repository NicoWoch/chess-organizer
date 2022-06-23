from abc import ABC, abstractmethod
from typing import List, Tuple

from src.objects.player import Player
from src.objects.round import Round, Result


class Algorithm(ABC):
    @abstractmethod
    def init_players(self, players: List[Player]): ...

    @abstractmethod
    def pair_players(self, last_rounds: List[Round]) -> List[Tuple[Player]]: ...

    @abstractmethod
    def result_to_points(self, result: Result) -> Tuple[int, int]: ...

    @abstractmethod
    def finish_round(self, round_: Round): ...

    @abstractmethod
    def update_ranking(self, players: List[Player], rounds: List[Round]): ...
