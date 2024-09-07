import unittest

from src.tournament.player import Player
from src.tournament.tournament import Tournament, RoundNotCompletedError
from src.tournament.round import Round


class Test1(unittest.TestCase):
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
        self.t.next_round(Round(7, ((0, 3), (1, 4), (2, 5))))

        self.t.set_result(0, 1, 0)
        self.t.set_result(1, 1, 0)
        self.t.set_result(2, .5, .5)

    def _add_sample_round_1(self):
        self.t.next_round(Round(7, ((1, 2), (3, 4), (5, 6))))

        self.t.set_result(0, 1, 0)
        self.t.set_result(1, 1, 0)
        self.t.set_result(2, 0, 1)

    def _assert_round_0_1_stats(self):
        stats = self.t.stats

        self.assertEqual(1, stats.played_together[0, 3])
        self.assertEqual(1, stats.played_together[3, 4])
        self.assertEqual(1, stats.played_as_a[0])
        self.assertEqual(-2, stats.floaters[4])
        self.assertEqual(2, stats.points[1])
        self.assertEqual(.5, stats.points[2])
        self.assertEqual(1, stats.points[3])
        self.assertEqual({6}, self.t.get_round(0).pause)
        self.assertEqual({0}, self.t.get_round(1).pause)
        self.assertEqual({0}, self.t.get_round().pause)

    def test_basic(self):
        self._add_sample_round_0()

        self.t.remove_result(2)
        self.assertRaises(RoundNotCompletedError, self.t.next_round, Round(7, ((0, 2),)))
        self.t.set_result(2, .5, .5)

        round_0 = self.t.get_round_stats(0)

        self.assertEqual(1, round_0.played_together[0, 3])
        self.assertEqual(0, round_0.played_together[3, 4])
        self.assertEqual(1, round_0.played_as_a[0])
        self.assertEqual(-1, round_0.floaters[4])
        self.assertEqual(0, round_0.points[4])
        self.assertEqual(.5, round_0.points[5])
        self.assertEqual({6}, self.t.get_round().pause)

        self._add_sample_round_1()

        round_1 = self.t.get_round_stats()

        self.assertEqual(0, round_1.played_together[0, 3])
        self.assertEqual(1, round_1.played_together[3, 4])
        self.assertEqual(0, round_1.played_as_a[0])
        self.assertEqual(-1, round_1.floaters[4])
        self.assertEqual(1, round_1.points[1])

        self._assert_round_0_1_stats()

    def test_round_removal(self):
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

    def test_wrong_pairing(self):
        pairs = ((1, 20), (3, 4))
        self.assertRaises(ValueError, lambda: self.t.next_round(Round(10, pairs)))

        pairs = ((1, 2), (100, 3))
        self.assertRaises(ValueError, lambda: self.t.next_round(Round(100, pairs)))


if __name__ == '__main__':
    unittest.main()
