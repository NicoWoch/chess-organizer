from src.tournament.round import Round
from src.tournament.round_stats import RoundStats
from src.tournament.scoring.scorer import Scorer, Score


class PointsScorer(Scorer):
    def __init__(self, *, pause_points: float):
        self.pause_points = pause_points

    def calculate_scores(self, no_players: int, rounds: list[Round], stats: RoundStats) -> tuple[Score, ...]:
        points = [0 for _ in range(no_players)]

        for round_ in rounds:
            for (player_a, player_b), result in zip(round_.pairs, round_.results):
                if result is None:
                    continue

                points[player_a] += result.points_a
                points[player_b] += result.points_b

            for pause in round_.pause:
                points[pause] += self.pause_points

        return tuple((p,) for p in points)
