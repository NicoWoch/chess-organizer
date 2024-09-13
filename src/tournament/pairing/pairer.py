from abc import abstractmethod, ABC

from src.tournament.round_stats import RoundStats
from src.tournament.round import Pairs


class Pairer(ABC):
    players: set[int]
    stats: RoundStats

    def pair(self, players: set[int], stats: RoundStats) -> Pairs:
        self.players = players
        self.stats = stats

        return self.__pair()

    @abstractmethod
    def __pair(self) -> Pairs: ...
