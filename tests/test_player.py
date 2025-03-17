import unittest

from src.player import *


class TestPlayer(unittest.TestCase):
    def test_constructor_title_name(self):
        player = Player.create_player(name='name', surname='surname', rating=1000)

        self.assertEqual(player.name, 'Name')
        self.assertEqual(player.surname, 'Surname')

    def test_player_eq(self):
        player1 = Player.create_player(name='name', surname='surname', rating=1000)
        player2 = Player.create_player(
            name='name', surname='surname', rating=1999
        )
        self.assertEqual(player1, player2)


if __name__ == '__main__':
    unittest.main()
