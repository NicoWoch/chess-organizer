import unittest
from typing import Iterable

from src.tournament.round import Round
from src.tournament.round_stats import RoundStats


def assert_iterable_dict(self: unittest.TestCase, iterable: Iterable, dict_: dict):
    for i, item in enumerate(iterable):
        if dict_[i] != item:
            self.assertEqual(iterable, dict_, 'failed in assert_iterable_dict()')


class TestSimple(unittest.TestCase):
    def setUp(self):
        self.rounds: list[Round] = [Round(4, ((0, 1), (2, 3)))]

        self.last_round.set_result(0, 1, 0)
        self.last_round.set_result(1, .5, .5)

        self.rounds.append(Round(4, ((0, 3), (1, 2))))

        self.last_round.set_result(0, 1, 0)
        self.last_round.set_result(1, .5, .5)

    @property
    def last_round(self):
        return self.rounds[-1]

    def test_points_calculation_one_round(self):
        stats = RoundStats.make_from_round(self.rounds[0])
        assert_iterable_dict(self, [1, 0, .5, .5], stats.points)

    def test_points_calculation_two_rounds(self):
        stats = RoundStats.make_from_rounds(self.rounds)
        assert_iterable_dict(self, [2, .5, 1, .5], stats.points)

    def test_round_count(self):
        stats = RoundStats.make_from_rounds(self.rounds[:1])
        self.assertEqual(1, stats.round_count)

        stats = RoundStats.make_from_rounds(self.rounds)
        self.assertEqual(2, stats.round_count)

    def test_played_as_side(self):
        stats = RoundStats.make_from_rounds(self.rounds)
        assert_iterable_dict(self, [2, 1, 1, 0], stats.played_as_a)
        assert_iterable_dict(self, [0, 1, 1, 2], stats.played_as_b)

    def test_played_together(self):
        stats = RoundStats.make_from_rounds(self.rounds)
        self.assertEqual(1, stats.played_together[0, 1])
        self.assertEqual(0, stats.played_together[1, 1])
        self.assertEqual(1, stats.played_together[2, 3])
        self.assertEqual(1, stats.played_together[3, 0])

    def test_floaters(self):
        stats = RoundStats.make_from_rounds(self.rounds)

        assert_iterable_dict(self, [2, 1, -1, -2], stats.floaters)

    def test_paused(self):
        stats = RoundStats.make_from_round(self.rounds[0])
        assert_iterable_dict(self, [0, 0, 0, 0], stats.paused)

        stats = RoundStats.make_from_rounds(self.rounds)
        assert_iterable_dict(self, [0, 0, 0, 0], stats.paused)


class TestMoreComplexRounds(unittest.TestCase):
    def setUp(self):
        self.rounds = [
            Round(10, ((9, 0), (3, 2), (1, 6), (5, 4))),
            Round(10, ((6, 1), (5, 2), (4, 8), (7, 3))),
            Round(10, ((2, 0), (1, 4), (6, 3), (5, 8), (9, 7))),
            Round(10, ((9, 0), (8, 1), (7, 2), (6, 3), (5, 4))),
        ]

        stat_round_1 = RoundStats.make_from_round(self.rounds[0])

        self.stats_by_round = [
            stat_round_1,
            stat_round_1 + RoundStats.make_from_round(self.rounds[1]),
            RoundStats.make_from_rounds(self.rounds[:3]),
            RoundStats.make_from_rounds(self.rounds),
        ]

    def test_round_count(self):
        self.assertEqual(1, self.stats_by_round[0].round_count)
        self.assertEqual(2, self.stats_by_round[1].round_count)
        self.assertEqual(3, self.stats_by_round[2].round_count)
        self.assertEqual(4, self.stats_by_round[3].round_count)

    def test_played_as_side(self):
        assert_iterable_dict(self, [0, 1, 0, 1, 0, 1, 0, 0, 0, 1], self.stats_by_round[0].played_as_a)
        assert_iterable_dict(self, [1, 0, 1, 0, 1, 0, 1, 0, 0, 0], self.stats_by_round[0].played_as_b)

        assert_iterable_dict(self, [0, 1, 0, 1, 1, 2, 1, 1, 0, 1], self.stats_by_round[1].played_as_a)
        assert_iterable_dict(self, [1, 1, 2, 1, 1, 0, 1, 0, 1, 0], self.stats_by_round[1].played_as_b)

        assert_iterable_dict(self, [0, 2, 1, 1, 1, 3, 2, 1, 0, 2], self.stats_by_round[2].played_as_a)
        assert_iterable_dict(self, [2, 1, 2, 2, 2, 0, 1, 1, 2, 0], self.stats_by_round[2].played_as_b)

        assert_iterable_dict(self, [0, 2, 1, 1, 1, 4, 3, 2, 1, 3], self.stats_by_round[3].played_as_a)
        assert_iterable_dict(self, [3, 2, 3, 3, 3, 0, 1, 1, 2, 0], self.stats_by_round[3].played_as_b)

    def test_floaters(self):
        assert_iterable_dict(self, [-1, 1, -1, 1, -1, 1, -1, 0, 0, 1], self.stats_by_round[0].floaters)
        assert_iterable_dict(self, [-1, -1, -2, -1, 1, 2, 1, 1, -1, 1], self.stats_by_round[1].floaters)
        assert_iterable_dict(self, [-2, 1, 1, -2, -1, 3, 2, -1, -2, 2], self.stats_by_round[2].floaters)
        assert_iterable_dict(self, [-3, -1, -1, -3, -2, 4, 3, 1, 1, 3], self.stats_by_round[3].floaters)

    def test_played_together(self):
        tests = [
            {(0, 0): 0, (0, 9): 1, (1, 6): 1, (8, 7): 0},
            {(2, 5): 1, (1, 6): 2},
            {(0, 9): 1, (3, 6): 1, (5, 8): 1},
            {(0, 9): 2, (3, 6): 2, (1, 4): 1, (4, 5): 2, (1, 9): 0},
        ]

        for stats, (test_id, test) in zip(self.stats_by_round, enumerate(tests)):
            for pair, count in test.items():
                msg = f'failed at round {test_id + 1} with pair {pair}'
                self.assertEqual(count, stats.played_together[pair], msg)
                self.assertEqual(count, stats.played_together[pair[::-1]], msg + ' reversed')

    def test_points(self):
        results_by_round = (
            ((0, 1), (0, 1), (0, 1), (1, 0)),
            ((0, 1), (0, 1), (1, 0), (.5, .5)),
            ((0, 1), (0, 1), (1, 0), (1, 0), (.5, .5)),
            ((0, 1), (1, 0), (0, 1), (0, 1), (1, 0)),
        )

        for round_, results in zip(self.rounds, results_by_round):
            for table_id, result in enumerate(results):
                round_.set_result(table_id, *result)

        stats = RoundStats.make_from_round(self.rounds[0])
        assert_iterable_dict(self, [1, 0, 1, 0, 0, 1, 1, 0, 0, 0], stats.points)
        stats += RoundStats.make_from_round(self.rounds[1])
        assert_iterable_dict(self, [1, 1, 2, .5, 1, 1, 1, .5, 0, 0], stats.points)
        stats += RoundStats.make_from_round(self.rounds[2])
        assert_iterable_dict(self, [2, 1, 2, .5, 2, 2, 2, 1, 0, .5], stats.points)
        stats += RoundStats.make_from_round(self.rounds[3])
        assert_iterable_dict(self, [3, 1, 3, 1.5, 2, 3, 2, 1, 1, .5], stats.points)

    def test_paused(self):
        stats = RoundStats.make_from_round(self.rounds[0])
        assert_iterable_dict(self, [0, 0, 0, 0, 0, 0, 0, 1, 1, 0], stats.paused)

        stats = RoundStats.make_from_rounds(self.rounds[:2])
        assert_iterable_dict(self, [1, 0, 0, 0, 0, 0, 0, 1, 1, 1], stats.paused)

        stats = RoundStats.make_from_rounds(self.rounds[:3])
        assert_iterable_dict(self, [1, 0, 0, 0, 0, 0, 0, 1, 1, 1], stats.paused)

        stats = RoundStats.make_from_rounds(self.rounds[:4])
        assert_iterable_dict(self, [1, 0, 0, 0, 0, 0, 0, 1, 1, 1], stats.paused)

    def test_paused_2_independent_of_class(self):
        rounds = [
            Round(10, ((9, 0), (3, 2))),
            Round(10, ((6, 1), (5, 2))),
            Round(10, ((2, 3), (5, 1))),
            Round(10, ((4, 8), (2, 5))),
            Round(10, ((8, 9), (3, 0))),
        ]

        stats = RoundStats.make_from_rounds(rounds[:1])
        assert_iterable_dict(self, [0, 1, 0, 0, 1, 1, 1, 1, 1, 0], stats.paused)
        stats = RoundStats.make_from_rounds(rounds[:2])
        assert_iterable_dict(self, [1, 1, 0, 1, 2, 1, 1, 2, 2, 1], stats.paused)
        stats = RoundStats.make_from_rounds(rounds[:3])
        assert_iterable_dict(self, [2, 1, 0, 1, 3, 1, 2, 3, 3, 2], stats.paused)
        stats = RoundStats.make_from_rounds(rounds[:4])
        assert_iterable_dict(self, [3, 2, 0, 2, 3, 1, 3, 4, 3, 3], stats.paused)
        stats = RoundStats.make_from_rounds(rounds[:5])
        assert_iterable_dict(self, [3, 3, 1, 2, 4, 2, 4, 5, 3, 3], stats.paused)


if __name__ == '__main__':
    unittest.main()
