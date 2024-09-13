import unittest
from typing import Iterable

from src.tournament.round import Round, GameResult
from src.tournament.round_stats import RoundStats


def assert_iterable_dict(self: unittest.TestCase, iterable: Iterable, dict_: dict):
    for i, item in enumerate(iterable):
        if dict_[i] != item:
            self.assertEqual(iterable, dict_, 'failed in assert_iterable_dict()')


class TestSimple(unittest.TestCase):
    def setUp(self):
        self.rounds: list[Round] = [Round(5, ((0, 1), (2, 3)))]
        self.starting_ratings = (1000, 1500, 1000, 1200, 1000)

        self.last_round.set_result(0, GameResult.WIN)
        self.last_round.set_result(1, GameResult.DRAW)

        self.rounds.append(Round(5, ((0, 3), (1, 4))))

        self.last_round.set_result(0, GameResult.WIN)
        self.last_round.set_result(1, GameResult.WIN)

        self.stats = RoundStats(5, self.starting_ratings, 32)
        self.stats.add_round(self.rounds[0])
        self.stats.add_round(self.rounds[1])

    @property
    def last_round(self):
        return self.rounds[-1]

    def test_round_count(self):
        stats = RoundStats(5, self.starting_ratings, 32)
        self.assertEqual(0, stats.round_count)
        stats.add_round(self.rounds[0])
        self.assertEqual(1, stats.round_count)
        stats.add_round(self.rounds[1])
        self.assertEqual(2, stats.round_count)

    def test_played_together(self):
        self.assertEqual(1, self.stats.played_together[0][1])
        self.assertEqual(1, self.stats.played_together[1][0])
        self.assertEqual(0, self.stats.played_together[1][1])
        self.assertEqual(0, self.stats.played_together[1][2])
        self.assertEqual(0, self.stats.played_together[1][3])
        self.assertEqual(1, self.stats.played_together[2][3])
        self.assertEqual(1, self.stats.played_together[3][2])
        self.assertEqual(1, self.stats.played_together[1][4])
        self.assertEqual(1, self.stats.played_together[4][1])

    def test_played_sides(self):
        self.assertEqual([2, 1, 1, 0, 0], self.stats.played_as_a)
        self.assertEqual([0, 1, 0, 2, 1], self.stats.played_as_b)

    def test_paused(self):
        stats = RoundStats(5, self.starting_ratings, 32)
        stats.add_round(self.rounds[0])
        self.assertEqual([0, 0, 0, 0, 1], stats.paused)
        stats.add_round(self.rounds[1])
        self.assertEqual([0, 0, 1, 0, 1], stats.paused)

    def test_floaters(self):
        self.assertEqual([2, 1, 1, -2, -1], self.stats.floaters)

    def test_wins_draws_losses(self):
        self.assertEqual([[1, 3], [4], [], [], []], self.stats.wins)
        self.assertEqual([[], [], [3], [2], []], self.stats.draws)
        self.assertEqual([[], [0], [], [0], [1]], self.stats.losses)

    def test_ratings(self):
        stats = RoundStats(5, self.starting_ratings, 32)
        stats.add_round(self.rounds[0])
        rating_changes_round_0 = (+30.296, -30.296, +8.312, -8.312, 0)

        for i, rating_change in enumerate(rating_changes_round_0):
            new_rating = self.starting_ratings[i] + rating_change
            self.__assert_rating_change(stats, i, rating_change, new_rating)

        stats.add_round(self.rounds[1])
        rating_changes_round_1 = (+22.940, +2.008, 0, -22.940, -2.008)

        for i, (rc1, rc2) in enumerate(zip(rating_changes_round_0, rating_changes_round_1)):
            new_rating = self.starting_ratings[i] + rc1 + rc2
            self.__assert_rating_change(stats, i, rc2, new_rating)

    def __assert_rating_change(self, stats: RoundStats, player: int, rating_change: float, new_rating: float):
        if rating_change > 0:
            self.assertGreater(stats.recent_rating_changes[player], 0)
        elif rating_change < 0:
            self.assertLess(stats.recent_rating_changes[player], 0)
        else:
            self.assertEqual(0, stats.recent_rating_changes[player])

        msg = f'Rating of player {player}, {stats.ratings[player]} is not close to expected {new_rating}'
        self.assertAlmostEqual(new_rating, stats.ratings[player], delta=2.0, msg=msg)


class TestMoreComplexRounds(unittest.TestCase):
    def setUp(self):
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
        self.stats_by_round: list[RoundStats] = []

        stats = RoundStats(10, self.starting_ratings, 32)
        stats.add_round(self.rounds[0])
        self.stats_by_round.append(stats.deepcopy())
        stats.add_round(self.rounds[1])
        self.stats_by_round.append(stats.deepcopy())
        stats.add_round(self.rounds[2])
        self.stats_by_round.append(stats.deepcopy())
        stats.add_round(self.rounds[3])
        self.stats_by_round.append(stats.deepcopy())

    def test_round_count(self):
        self.assertEqual(1, self.stats_by_round[0].round_count)
        self.assertEqual(2, self.stats_by_round[1].round_count)
        self.assertEqual(3, self.stats_by_round[2].round_count)
        self.assertEqual(4, self.stats_by_round[3].round_count)

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
                self.assertEqual(count, stats.played_together[pair[0]][pair[1]], msg)
                self.assertEqual(count, stats.played_together[pair[1]][pair[0]], msg + ' reversed')

    def test_played_sides(self):
        self.assertEqual([0, 1, 0, 1, 0, 1, 0, 0, 0, 1], self.stats_by_round[0].played_as_a)
        self.assertEqual([1, 0, 1, 0, 1, 0, 1, 0, 0, 0], self.stats_by_round[0].played_as_b)

        self.assertEqual([0, 1, 0, 1, 1, 2, 1, 1, 0, 1], self.stats_by_round[1].played_as_a)
        self.assertEqual([1, 1, 2, 1, 1, 0, 1, 0, 1, 0], self.stats_by_round[1].played_as_b)

        self.assertEqual([0, 2, 1, 1, 1, 3, 2, 1, 0, 2], self.stats_by_round[2].played_as_a)
        self.assertEqual([2, 1, 2, 2, 2, 0, 1, 1, 2, 0], self.stats_by_round[2].played_as_b)

        self.assertEqual([0, 2, 1, 1, 1, 4, 3, 2, 1, 3], self.stats_by_round[3].played_as_a)
        self.assertEqual([3, 2, 3, 3, 3, 0, 1, 1, 2, 0], self.stats_by_round[3].played_as_b)

    def test_paused(self):
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 1, 1, 0], self.stats_by_round[0].paused)
        self.assertEqual([1, 0, 0, 0, 0, 0, 0, 1, 1, 1], self.stats_by_round[1].paused)
        self.assertEqual([1, 0, 0, 0, 0, 0, 0, 1, 1, 1], self.stats_by_round[2].paused)
        self.assertEqual([1, 0, 0, 0, 0, 0, 0, 1, 1, 1], self.stats_by_round[3].paused)

    def test_floaters(self):
        self.assertEqual([-1, 1, -1, 1, -1, 1, -1, 0, 0, 1], self.stats_by_round[0].floaters)
        self.assertEqual([-1, -1, -2, -1, 1, 2, 1, 1, -1, 1], self.stats_by_round[1].floaters)
        self.assertEqual([-2, 1, 1, -2, -1, 3, 2, -1, -2, 2], self.stats_by_round[2].floaters)
        self.assertEqual([-3, -1, -1, -3, -2, 4, 3, 1, 1, 3], self.stats_by_round[3].floaters)

    def test_wins_draws_losses(self):
        self.assertEqual([[9, 2, 9], [6], [3, 5, 7], [6], [8, 1], [4, 8, 4], [1, 3], [], [1], []],
                         self.stats_by_round[3].wins)
        self.assertEqual([[], [], [], [7], [], [], [], [3, 9], [], [7]], self.stats_by_round[3].draws)
        self.assertEqual([[], [6, 4, 8], [0], [2, 6], [5, 5], [2], [1, 3], [2], [4, 5], [0, 0]],
                         self.stats_by_round[3].losses)

    def test_ratings_very_basic(self):
        self.assertGreater(self.stats_by_round[-1].ratings[0], self.starting_ratings[0])
        self.assertLess(self.stats_by_round[-1].ratings[9], self.starting_ratings[9])

    def test_recent_rating_changes_signs(self):
        for i, (round_, stats) in enumerate(zip(self.rounds, self.stats_by_round)):
            is_ok = True

            for (player_a, player_b), game_result in zip(round_.pairs, round_.results):
                if game_result == GameResult.WIN:
                    is_ok = is_ok and (stats.recent_rating_changes[player_a] > 0)
                    is_ok = is_ok and (stats.recent_rating_changes[player_b] < 0)
                elif game_result == GameResult.LOSE:
                    is_ok = is_ok and (stats.recent_rating_changes[player_a] < 0)
                    is_ok = is_ok and (stats.recent_rating_changes[player_b] > 0)

            if not is_ok:
                self.fail(f'Recent rating changes signs not match on round {i}')


class TestPauseComplex(unittest.TestCase):
    def test_paused(self):
        rounds = [
            Round(10, ((9, 0), (3, 2))),
            Round(10, ((6, 1), (5, 2))),
            Round(10, ((2, 3), (5, 1))),
            Round(10, ((4, 8), (2, 5))),
            Round(10, ((8, 9), (3, 0))),
        ]

        stats = RoundStats(10, tuple([1000] * 10), 32)
        stats.add_round(rounds[0])
        self.assertEqual([0, 1, 0, 0, 1, 1, 1, 1, 1, 0], stats.paused)
        stats.add_round(rounds[1])
        self.assertEqual([1, 1, 0, 1, 2, 1, 1, 2, 2, 1], stats.paused)
        stats.add_round(rounds[2])
        self.assertEqual([2, 1, 0, 1, 3, 1, 2, 3, 3, 2], stats.paused)
        stats.add_round(rounds[3])
        self.assertEqual([3, 2, 0, 2, 3, 1, 3, 4, 3, 3], stats.paused)
        stats.add_round(rounds[4])
        self.assertEqual([3, 3, 1, 2, 4, 2, 4, 5, 3, 3], stats.paused)


if __name__ == '__main__':
    unittest.main()
