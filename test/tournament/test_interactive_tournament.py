import unittest

from src.tournament.interactive_tournament import InteractiveTournament
from src.tournament.player import Player
from src.tournament.round import GameResult


class TestSimple(unittest.TestCase):
    def setUp(self):
        self.it = InteractiveTournament()

    def __add_sample_players(self) -> tuple[Player, ...]:
        p1 = Player('Adam Nowak', 1200)
        p2 = Player('Borys Kowalski', 1500)
        p3 = Player('Celina Cebula', 900)
        self.it.add_player(p1)
        self.it.add_player(p2)
        self.it.add_player(p3)

        return p1, p2, p3

    def test_adding_removing_players(self):
        p1, p2, p3 = self.__add_sample_players()

        self.it.remove_player(Player('Borys Kowalski'))
        self.it.add_player(p2)

        self.it.remove_player(Player('Borys Kowalski'))
        self.it.remove_player(Player('Borys Kowalski'))
        self.it.add_player(p2)

        self.assertRaises(ValueError, self.it.add_player, p1)
        self.assertRaises(ValueError, self.it.add_player, p2)
        self.assertRaises(ValueError, self.it.add_player, p3)

        self.assertEqual(3, len(self.it.players))
        self.assertFalse(self.it.is_running())
        self.assertFalse(self.it.is_finished())

    def test_tournament_with_one_round(self):
        self.assertFalse(self.it.is_running())
        self.assertFalse(self.it.is_finished())

        self.__add_sample_players()

        self.it.next_round(((0, 1),))

        self.it.set_result(0, GameResult.WIN)
        self.assertEqual([1, 0, 1], [p[0] for p in self.it.get_scores()])

        self.it.set_result(0, None)
        self.assertEqual([0, 0, 1], [p[0] for p in self.it.get_scores()])

        self.it.set_result(0, GameResult.LOSE)
        self.it.set_result(0, GameResult.DRAW)
        self.assertEqual([.5, .5, 1], [p[0] for p in self.it.get_scores()])

        self.assertTrue(self.it.is_running())
        self.assertFalse(self.it.is_finished())

        self.it.finish()

        self.assertFalse(self.it.is_running())
        self.assertTrue(self.it.is_finished())

        self.assertEqual([.5, .5, 1], [p[0] for p in self.it.get_scores()])


if __name__ == '__main__':
    unittest.main()
