import unittest
from src.player.player import *


class TestPlayer(unittest.TestCase):
    # def test_constructor_and_get_data(self):
    #     self.assertEqual(Player('name', 'surname', 1000, [[0, 100], [10, 1200]]).get_data(),
    #                            ['name', 'surname', 1000, [[0, 100], [10, 1200]]])
    #
    # def test_player_eq(self):
    #     player = Player('X', 'Y', 1234, [[0, 1000]])
    #     self.assertEqual(player, player)
    #
    # def test_player_not_eq(self):
    #     player1 = Player('X', 'Y', 1234, [[0, 1000]])
    #     player2 = Player('X', 'Y', 1234, [[0, 1020]])
    #     self.assertNotEqual(player1, player2)
    #
    # def test_saving_and_loading_players(self):
    #     players = [Player(f'name {i}', f'surname {i}', i * 100, [[i, i + 2]]) for i in range(20)]
    #     save_players(players, 'temp_players.json')
    #     players2 = load_players('temp_players.json')
    #
    #     for p1, p2 in zip(players, players2):
    #         if p1 != p2:
    #             self.fail(f'{p2} should equal {p1}')
    ...


if __name__ == '__main__':
    unittest.main()
