from src.tournament.round_stats import RoundStats
from src.tournament.tournament import Pairer


class SwissPairing(Pairer):
    players: set[int]
    stats: RoundStats

    def __pair(self) -> tuple[tuple[int, int], ...]:
        return ()
