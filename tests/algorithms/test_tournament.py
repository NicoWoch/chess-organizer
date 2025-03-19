import random
import unittest

from src.algorithms.constants import Points, Result
from src.algorithms.errors import TournamentNotRunningError
from src.algorithms.tournament import Tournament, Pairing
from src.dummy_generator import get_random_players


class DummyTournament(Tournament):
    def _get_default_points(self) -> Points:
        return Points(3)

    def _pair_round(self, round_no: int) -> Pairing:
        raise NotImplementedError

    def _update_small_points(self):
        raise NotImplementedError


class TestTournament(unittest.TestCase):
    def setUp(self):
        self.tournament = DummyTournament('tournament')
        self.players = get_random_players(50, rng=random.Random(235))

        self.tournament.add_players(self.players)

    def test_constructor_title(self):
        t = DummyTournament('hello')
        self.assertEqual(t.name, 'hello')

    def test_constructor_and_getters(self):
        self.assertEqual(self.tournament.players, self.players)
        self.assertNotEqual(id(self.tournament.players), id(self.players))

        for i in range(len(self.players)):
            self.assertEqual(self.tournament.get_points(i).big_points, 0)
            self.assertEqual(self.tournament.get_points(i).small_points, (0, 0, 0))
            self.assertEqual(list(self.tournament.get_opponents(i).values()), [[]] * 3)
            self.assertEqual(self.tournament.round_count, 0)

    def test_errors(self):
        self.assertRaises(TournamentNotRunningError, lambda: self.tournament.set_result(0, Result.White))
        self.assertRaises(TournamentNotRunningError, lambda: self.tournament.end_tournament())


if __name__ == '__main__':
    unittest.main()
