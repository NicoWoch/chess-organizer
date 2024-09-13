from src.tournament.round import Round
from src.tournament.round_stats import RoundStats
from src.tournament.scoring.points_scorer import PointsScorer
from src.tournament.scoring.scorer import Score


class BuchholzScorer(PointsScorer):
    def __init__(self, *, pause_points: float = 1, win_mul: float = 3, draw_mul: float = 1, lose_mul: float = 1):
        super().__init__(pause_points=pause_points)
        self.win_mul = win_mul
        self.draw_mul = draw_mul
        self.lose_mul = lose_mul

    def calculate_scores(self, no_players: int, rounds: list[Round], stats: RoundStats) -> tuple[Score, ...]:
        big_points = [score for score, *_ in super().calculate_scores(no_players, rounds, stats)]
        scores: list[Score | None] = [None for _ in range(no_players)]

        for i in range(no_players):
            win_points = sum(big_points[winned] for winned in stats.wins[i])
            draw_points = sum(big_points[drawed] for drawed in stats.draws[i])
            lose_points = sum(big_points[lost] for lost in stats.losses[i])

            scores[i] = (
                big_points[i],
                win_points * self.win_mul + draw_points * self.draw_mul,
                lose_points * self.lose_mul,
            )

        return tuple(scores)
