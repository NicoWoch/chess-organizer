import unittest

from src.player import *


class TestPlayer(unittest.TestCase):
    def test_constructor_title_name(self):
        player = Player('name', 'surname', Gender.Men, 1000)

        self.assertEqual(player.name, 'Name')
        self.assertEqual(player.surname, 'Surname')

    def test_player_eq(self):
        player1 = Player('X', 'Y', Gender.Men, 1000)
        player2 = Player('X', 'Y', Gender.Women, 1200)
        self.assertEqual(player1, player2)

    def test_player_not_eq(self):
        player1 = Player('X', 'Y', Gender.Men, 1200)
        player2 = Player('X', 'not Y', Gender.Women, 1000)
        self.assertNotEqual(player1, player2)


class TestPlayerList(unittest.TestCase):
    def test_saving_and_loading_players(self):
        player_list = PlayerList([Player(f'name {i}', f'surname {i}', Gender.Other, 101 * i + 1008) for i in range(10)])

        player_list.save_players('temp_players.players')
        player_list_2 = PlayerList.load_players('temp_players.players')

        self.assertEqual(player_list, player_list_2)


if __name__ == '__main__':
    unittest.main()
