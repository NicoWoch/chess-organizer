import unittest

from src.tournament.round import Round


class Test1(unittest.TestCase):
    def setUp(self):
        self.sample_pairs = ((1, 2), (3, 4), (5, 6))
        self.sample_round = Round(7, self.sample_pairs)

    def test_setting_results(self):
        self.sample_round.set_result(0, .5, .5)
        self.sample_round.set_result(1, 0, 1)
        self.sample_round.set_result(2, 1, 0)

        self.assertEqual(7, self.sample_round.no_players)
        self.assertEqual(self.sample_pairs, self.sample_round.pairs)
        self.assertEqual([(.5, .5), (0, 1), (1, 0)], self.sample_round.results)
        self.assertEqual({0}, self.sample_round.pause)

    def test_removing_reseting_results(self):
        self.sample_round.set_result(0, .5, .5)
        self.sample_round.set_result(1, 0, 1)
        self.sample_round.set_result(2, 1, 0)
        self.sample_round.remove_result(2)
        self.sample_round.set_result(1, 1, 0)

        self.assertEqual(7, self.sample_round.no_players)
        self.assertEqual(self.sample_pairs, self.sample_round.pairs)
        self.assertEqual([(.5, .5), (1, 0), None], self.sample_round.results)
        self.assertEqual({0}, self.sample_round.pause)

    def test_is_complete(self):
        self.assertFalse(self.sample_round.is_completed())

        self.sample_round.set_result(0, .5, .5)
        self.assertFalse(self.sample_round.is_completed())

        self.sample_round.set_result(1, 0, 1)
        self.assertFalse(self.sample_round.is_completed())

        self.sample_round.set_result(2, 1, 0)
        self.assertTrue(self.sample_round.is_completed())

        self.sample_round.remove_result(2)
        self.assertFalse(self.sample_round.is_completed())

    def test_invald_pairing(self):
        pairs = ((1, 2), (3, 4), (5, 5))
        self.assertRaises(ValueError, lambda: Round(10, pairs))

        pairs = ((1, 2), (3, 4), (5, 4))
        self.assertRaises(ValueError, lambda: Round(10, pairs))

        pairs = ()
        self.assertRaises(ValueError, lambda: Round(10, pairs))

        pairs = ((-1, 2),)
        self.assertRaises(ValueError, lambda: Round(10, pairs))

        pairs = ((5, 3), (1, 2))
        self.assertRaises(ValueError, lambda: Round(5, pairs))


if __name__ == '__main__':
    unittest.main()
