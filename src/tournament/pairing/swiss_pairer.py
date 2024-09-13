from src.tournament.round_stats import RoundStats
from src.tournament.tournament import Pairer
from src.tournament.round import Pairs


class SwissPairing(Pairer):
    players: set[int]
    stats: RoundStats

    def __pair(self) -> Pairs:
        return ()
