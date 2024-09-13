from src.tournament.round import Round
from src.tournament.round_stats import RoundStats
from src.tournament.scoring.scorer import Scorer, Score


class BuchholzScorer(Scorer):
    def calculate_scores(self, no_players: int, rounds: list[Round], stats: RoundStats) -> tuple[Score, ...]:
        pass
