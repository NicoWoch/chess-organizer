import unittest

from src.tournament.player import Player
from src.tournament.scoring.points_scorer import PointsScorer
from src.tournament.tournament import Tournament, RoundNotCompletedError
from src.tournament.round import Round, GameResult


class TestSimple(unittest.TestCase):
    def setUp(self):
        self.t = Tournament((
            Player('Adam', 'A'),
            Player('Borys', 'B'),
            Player('Celina', 'C'),
            Player('Damian', 'D'),
            Player('Ewelina', 'E'),
            Player('Franek', 'F'),
            Player('Grażyna', 'G'),
        ))

    def _add_sample_round_0(self):
        self.t.next_round(((0, 3), (1, 4), (2, 5)))

        self.t.set_result(0, GameResult.WIN)
        self.t.set_result(1, GameResult.WIN)
        self.t.set_result(2, GameResult.DRAW)

    def _add_sample_round_1(self):
        self.t.next_round(((1, 2), (3, 4), (5, 6)))

        self.t.set_result(0, GameResult.WIN)
        self.t.set_result(1, GameResult.WIN)
        self.t.set_result(2, GameResult.LOSE)

    def _assert_round_0_1_stats(self):
        stats = self.t.stats

        self.assertEqual(1, stats.played_together[0][3])
        self.assertEqual(1, stats.played_together[3][4])
        self.assertEqual(1, stats.played_as_a[0])
        self.assertEqual(-2, stats.floaters[4])
        self.assertEqual({6}, self.t.get_round(0).pause)
        self.assertEqual({0}, self.t.get_round(1).pause)
        self.assertEqual({0}, self.t.get_round().pause)

    def test_basic(self):
        self._add_sample_round_0()

        self.t.set_result(2, None)
        self.assertRaises(RoundNotCompletedError, self.t.next_round, Round(7, ((0, 2),)))
        self.t.set_result(2, GameResult.DRAW)

        round_0 = self.t.get_stats(0)

        self.assertEqual(1, round_0.played_together[0][3])
        self.assertEqual(0, round_0.played_together[3][4])
        self.assertEqual(1, round_0.played_as_a[0])
        self.assertEqual(-1, round_0.floaters[4])
        self.assertEqual({6}, self.t.get_round().pause)

        self._add_sample_round_1()

        round_1 = self.t.get_stats()

        self.assertEqual(1, round_1.played_together[0][3])
        self.assertEqual(1, round_1.played_together[4][3])
        self.assertEqual(1, round_1.played_as_a[0])
        self.assertEqual(-2, round_1.floaters[4])

        self._assert_round_0_1_stats()

    def test_round_removal_stats_calculation(self):
        self._add_sample_round_0()
        self._add_sample_round_1()
        self.t.remove_last_round()
        self._add_sample_round_0()
        self.t.remove_last_round()
        self.t.remove_last_round()
        _ = self.t.stats

        self._add_sample_round_0()
        _ = self.t.stats

        self._add_sample_round_0()
        self.t.remove_last_round()
        _ = self.t.stats

        self._add_sample_round_1()
        _ = self.t.stats

        self._assert_round_0_1_stats()

    def test_wrong_and_good_pairings(self):
        pairs = ((1, 20), (3, 4))
        self.assertRaises(ValueError, self.t.next_round, pairs)

        pairs = ((1, 2), (7, 3))
        self.assertRaises(ValueError, self.t.next_round, pairs)

        pairs = ()
        self.t.next_round(pairs)
        self.t.remove_last_round()

    def test_scoreboard_with_points_scorer(self):
        self.t.settings.scorer = PointsScorer(pause_points=1)
        self._add_sample_round_0()
        self._add_sample_round_1()

        scores = ((2,), (2,), (.5,), (1,), (0,), (.5,), (2,))
        self.assertEqual(7, len(self.t.get_scores()))
        self.assertEqual(scores, self.t.get_scores())

        scoreboard = self.t.get_scoreboard()
        scoreboard_with_ids = [(place, self.t.players.index(player), score[0]) for (place, player, score) in scoreboard]

        self.assertEqual(7, len(scoreboard))
        self.assertEqual({(1, 0, 2), (1, 1, 2), (1, 6, 2)}, set(scoreboard_with_ids[:3]))
        self.assertEqual({(4, 3, 1)}, set(scoreboard_with_ids[3:4]))
        self.assertEqual({(5, 2, .5), (5, 5, .5)}, set(scoreboard_with_ids[4:6]))
        self.assertEqual({(7, 4, 0)}, set(scoreboard_with_ids[6:]))




if __name__ == '__main__':
    unittest.main()
