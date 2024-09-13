import unittest

from src.tournament.round import Round, GameResult
from src.tournament.round_stats import RoundStats
from src.tournament.scoring.buchholz_scorer import BuchholzScorer
from src.tournament.scoring.scorer import Score


class TestBuchholzScorer(unittest.TestCase):
    @staticmethod
    def __calculate_scores(rounds: list[Round], **kwargs) -> tuple[Score, ...]:
        sample_ratings = tuple(1000 for _ in range(rounds[0].no_players))
        stats = RoundStats(rounds[0].no_players, sample_ratings, 32)

        for round_ in rounds:
            stats.add_round(round_)

        return BuchholzScorer(**kwargs).calculate_scores(rounds[0].no_players, rounds, stats)

    @staticmethod
    def __from_sample_rounds_1() -> list[Round]:
        rounds = [
            Round(4, ((0, 1), (2, 3))),
            Round(4, ((0, 1), (2, 3))),
        ]

        rounds[0].set_result(0, GameResult.WIN)
        rounds[0].set_result(1, GameResult.WIN)
        rounds[1].set_result(0, GameResult.DRAW)
        rounds[1].set_result(1, GameResult.LOSE)

        return rounds

    def test_structure(self):
        rounds = self.__from_sample_rounds_1()
        scores = self.__calculate_scores(rounds)

        self.assertEqual(rounds[0].no_players, len(scores))

        for score in scores:
            self.assertIsInstance(score, tuple)
            self.assertEqual(3, len(score))

    def test_scores_from_sample_1(self):
        rounds = self.__from_sample_rounds_1()
        scores = self.__calculate_scores(rounds)

        self.assertEqual((
            (1.5, 2, 0),
            (.5, 1.5, 1.5),
            (1, 3, 1),
            (1, 3, 1),
        ), scores)


if __name__ == '__main__':
    unittest.main()
