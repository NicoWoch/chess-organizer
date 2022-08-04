import unittest

from src.player import *


class TestPlayer(unittest.TestCase):
    def test_constructor_title_name(self):
        player = Player.create_player(
            name='name', surname='surname', gender=Gender.Men, title='', rating=1000, group_name='default'
        )

        self.assertEqual(player.name, 'Name')
        self.assertEqual(player.surname, 'Surname')

    def test_player_eq(self):
        player1 = Player.create_player(
            name='name', surname='surname', gender=Gender.Men, title='', rating=1000, group_name='default'
        )
        player2 = Player.create_player(
            name='name', surname='surname', gender=Gender.Men, title='GM', rating=1999, group_name='default2'
        )
        self.assertEqual(player1, player2)


if __name__ == '__main__':
    unittest.main()
