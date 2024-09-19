from abc import abstractmethod, ABC

from src.tournament.round_stats import RoundStats
from src.tournament.round import Pairs
from src.tournament.scoring.scorer import Score

type ListPairs = list[tuple[int, int]]


class Pairer(ABC):
    players: tuple[int, ...]
    stats: RoundStats
    scores: tuple[Score, ...]

    def pair(self, enabled_players: tuple[int, ...], stats: RoundStats, scores: tuple[Score, ...]) -> Pairs:
        self.players = enabled_players
        self.stats = stats
        self.scores = scores

        return self._pair()

    @abstractmethod
    def _pair(self) -> Pairs: ...
