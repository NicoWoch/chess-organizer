import unittest

from src.tournament.round import Round, GameResult


class Test1(unittest.TestCase):
    def setUp(self):
        self.sample_pairs = ((1, 2), (3, 4), (5, 6))
        self.sample_round = Round(7, self.sample_pairs)

    def test_setting_results(self):
        self.sample_round.set_result(0, GameResult.DRAW)
        self.sample_round.set_result(1, GameResult.LOSE)
        self.sample_round.set_result(2, GameResult.WIN)

        self.assertEqual(7, self.sample_round.no_players)
        self.assertEqual(self.sample_pairs, self.sample_round.pairs)
        self.assertEqual([GameResult.DRAW, GameResult.LOSE, GameResult.WIN], self.sample_round.results)
        self.assertEqual({0}, self.sample_round.pause)

    def test_removing_reseting_results(self):
        self.sample_round.set_result(0, GameResult.DRAW)
        self.sample_round.set_result(1, GameResult.LOSE)
        self.sample_round.set_result(2, GameResult.WIN)
        self.sample_round.set_result(2, None)
        self.sample_round.set_result(1, GameResult.WIN)

        self.assertEqual(7, self.sample_round.no_players)
        self.assertEqual(self.sample_pairs, self.sample_round.pairs)
        self.assertEqual([GameResult.DRAW, GameResult.WIN, None], self.sample_round.results)
        self.assertEqual({0}, self.sample_round.pause)

    def test_is_complete(self):
        self.assertFalse(self.sample_round.is_completed())

        self.sample_round.set_result(0, GameResult.DRAW)
        self.assertFalse(self.sample_round.is_completed())

        self.sample_round.set_result(1, GameResult.LOSE)
        self.assertFalse(self.sample_round.is_completed())

        self.sample_round.set_result(2, GameResult.WIN)
        self.assertTrue(self.sample_round.is_completed())

        self.sample_round.set_result(2, None)
        self.assertFalse(self.sample_round.is_completed())

    def test_invald_pairing(self):
        pairs = ((1, 2), (3, 4), (5, 5))
        self.assertRaises(ValueError, lambda: Round(10, pairs))

        pairs = ((1, 2), (3, 4), (5, 4))
        self.assertRaises(ValueError, lambda: Round(10, pairs))

        pairs = ((-1, 2),)
        self.assertRaises(ValueError, lambda: Round(10, pairs))

        pairs = ((5, 3), (1, 2))
        self.assertRaises(ValueError, lambda: Round(5, pairs))

    def test_empty_pairing(self):
        round_1 = Round(0, ())
        self.assertEqual(0, round_1.no_players)
        self.assertEqual((), round_1.pairs)
        self.assertEqual(set(), round_1.pause)
        self.assertEqual([], round_1.results)

        round_2 = Round(4, ())
        self.assertEqual(4, round_2.no_players)
        self.assertEqual((), round_2.pairs)
        self.assertEqual({0, 1, 2, 3}, round_2.pause)
        self.assertEqual([], round_2.results)

if __name__ == '__main__':
    unittest.main()
