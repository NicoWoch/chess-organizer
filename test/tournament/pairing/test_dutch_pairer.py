import logging
import sys
import unittest

from src.tournament.pairing.dutch_pairer import DutchPairer
from src.tournament.round import Round, GameResult, Pairs
from src.tournament.round_stats import RoundStats
from src.tournament.scoring.points_scorer import PointsScorer

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])


class TestSwissPairing(unittest.TestCase):
    def test_basic(self):
        self.rounds = [
            Round(10, ((9, 0), (3, 2), (1, 6), (5, 4))),
            Round(10, ((6, 1), (5, 2), (4, 8), (7, 3))),
            Round(10, ((2, 0), (1, 4), (6, 3), (5, 8), (9, 7))),
            Round(10, ((9, 0), (8, 1), (7, 2), (6, 3), (5, 4))),
        ]

        results_by_round = (
            (GameResult.LOSE, GameResult.LOSE, GameResult.LOSE, GameResult.WIN),
            (GameResult.LOSE, GameResult.LOSE, GameResult.WIN, GameResult.DRAW),
            (GameResult.LOSE, GameResult.LOSE, GameResult.WIN, GameResult.WIN, GameResult.DRAW),
            (GameResult.LOSE, GameResult.WIN, GameResult.LOSE, GameResult.LOSE, GameResult.WIN),
        )

        for round_, results in zip(self.rounds, results_by_round):
            for table_id, result in enumerate(results):
                round_.set_result(table_id, result)

        self.starting_ratings = (1000, 1200, 1000, 1100, 1500, 1000, 1000, 1000, 1000, 1000)
        self.stats: RoundStats = RoundStats(10, self.starting_ratings, 32)

        self.pairer = DutchPairer()
        self.scorer = PointsScorer()
        pairs: list[Pairs] = [
            self.pairer.pair(tuple(range(10)), self.stats,
                             self.scorer.calculate_scores(10, self.rounds[:0], self.stats))
        ]
        print('First Pairing:', pairs[0], '\n')

        for i in range(len(self.rounds)):
            self.stats.add_round(self.rounds[i])
            pairs.append(self.pairer.pair(tuple(range(10)), self.stats,
                                          self.scorer.calculate_scores(10, self.rounds[:i + 1], self.stats)))

            print(f'Pairing of Round {i + 1}:', pairs[i + 1], '\n')

        self.fail('expected fail for now')  # TODO: remove later


if __name__ == '__main__':
    unittest.main()
