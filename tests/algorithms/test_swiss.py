import unittest

from src.algorithms.swiss_tournament import SwissTournament
from src.algorithms.tournament import Result, Round
from src.player import Player, Gender


def get_dummy():
    dummy_players = [
        Player.create_player(name='Adam', surname='Nowak', gender=Gender.Men, rating=1200),
        Player.create_player(name='Anna', surname='Nowak', gender=Gender.Women, rating=1100),
        Player.create_player(name='Maximum', surname='Engine', gender=Gender.Other, rating=3000),
        Player.create_player(name='Marcin', surname='Nowak', gender=Gender.Men, rating=800),
        Player.create_player(name='Maximum2', surname='Engine2', gender=Gender.Other, rating=3200),
        Player.create_player(name='Ryszard', surname='Nowak', gender=Gender.Men, rating=990),
        Player.create_player(name='2Adam', surname='Nowak', gender=Gender.Men, rating=1200),
        Player.create_player(name='2Anna', surname='Nowak', gender=Gender.Women, rating=1100),
        Player.create_player(name='2Maximum', surname='Engine', gender=Gender.Other, rating=3000),
        Player.create_player(name='2Marcin', surname='Nowak', gender=Gender.Men, rating=800),
        Player.create_player(name='2Maximum2', surname='Engine2', gender=Gender.Other, rating=3200),
        Player.create_player(name='2Ryszard', surname='Nowak', gender=Gender.Men, rating=990),
        Player.create_player(name='3Adam', surname='Nowak', gender=Gender.Men, rating=1200),
        Player.create_player(name='3Anna', surname='Nowak', gender=Gender.Women, rating=1100),
        Player.create_player(name='3Maximum', surname='Engine', gender=Gender.Other, rating=3000),
        Player.create_player(name='3Marcin', surname='Nowak', gender=Gender.Men, rating=800),
        Player.create_player(name='3Maximum2', surname='Engine2', gender=Gender.Other, rating=3200),
        Player.create_player(name='3Ryszard', surname='Nowak', gender=Gender.Men, rating=990),
        Player.create_player(name='4Adam', surname='Nowak', gender=Gender.Men, rating=1200),
        Player.create_player(name='4Anna', surname='Nowak', gender=Gender.Women, rating=1100),
        Player.create_player(name='4Maximum', surname='Engine', gender=Gender.Other, rating=3000),
        Player.create_player(name='4Marcin', surname='Nowak', gender=Gender.Men, rating=800),
        Player.create_player(name='4Maximum2', surname='Engine2', gender=Gender.Other, rating=3200),
        Player.create_player(name='4Ryszard', surname='Nowak', gender=Gender.Men, rating=990),
    ]
    return dummy_players


class TestSwiss(unittest.TestCase):
    def assert_round(self, round_: Round, pairs: list[tuple[Player, Player]]):
        for game in round_:
            for i, pair in enumerate(pairs):
                if game.white in pair and game.black in pair:
                    del pairs[i]
                    break
            else:
                self.fail(f'Bad pair {game.white} with {game.black}')

    def test_no_error(self):
        players = get_dummy()[:24]
        t = SwissTournament('t1', players)

        for _ in range(3):
            t.next_round()
            for i in range(12):
                t.set_result(i, Result.Black)
                t.set_result(i, Result.Draw)
                t.set_result(i, Result.Playing)
                t.set_result(i, Result.White)

    def test_pairing_1(self):
        players = get_dummy()[:4]
        t = SwissTournament('t2', players)

        t.next_round()
        t.set_result(0, Result.White)
        t.set_result(1, Result.White)
        games = t.active_round

        t.next_round()
        self.assert_round(t.active_round, [
            (games[0].white, games[1].white),
            (games[0].black, games[1].black)
        ])

    def test_pausing_player(self):
        players = get_dummy()[:23]
        t = SwissTournament('t3', players)

        t.next_round()
        for i in range(11):
            t.set_result(i, Result.White)

        pauses = [t.get_waiting_players()[0]]

        for _ in range(3):
            t.next_round()
            for i in range(11):
                t.set_result(i, Result.White)

            pause = t.get_waiting_players()[0]
            self.assertNotIn(pause, pauses)

            pauses.append(pause)

    def test_scoreboard_with_points(self):
        players = get_dummy()[:4]

        t = SwissTournament('t4', players)

        t.next_round()

        # Testing replace results
        t.set_result(0, Result.Draw)
        t.set_result(1, Result.Black)
        t.set_result(0, Result.Playing)

        t.set_result(0, Result.White)
        t.set_result(1, Result.Draw)

        games = t.active_round
        t.end_tournament()

        scoreboard = t.get_scoreboard()

        self.assertEqual(scoreboard[0][0], games[0].white)
        self.assertEqual(scoreboard[-1][0], games[0].black)

        self.assertEqual(scoreboard[0][1], (2, 0, 0))
        self.assertEqual(scoreboard[1][1], (1, 1, 0))
        self.assertEqual(scoreboard[2][1], (1, 1, 0))
        self.assertEqual(scoreboard[3][1], (0, 0, 2))

    def set_player_win(self, t: SwissTournament, player: Player):
        for i, game in enumerate(t.active_round):
            if player == game.white:
                t.set_result(i, Result.White)
            elif player == game.black:
                t.set_result(i, Result.Black)
        else:
            ValueError('Player not found')

    def set_player_lost(self, t: SwissTournament, player: Player):
        for i, game in enumerate(t.active_round):
            if player == game.white:
                t.set_result(i, Result.Black)
            elif player == game.black:
                t.set_result(i, Result.White)
        else:
            ValueError('Player not found')

    def test_points_1(self):
        players = get_dummy()[:4]

        t = SwissTournament('t5', players)
        t.next_round()

        # Testing replace results
        t.set_result(0, Result.Draw)
        t.set_result(1, Result.Black)
        t.set_result(0, Result.Playing)

        t.set_result(0, Result.White)
        t.set_result(1, Result.Draw)

        g1 = t.active_round
        a, b = g1[0].white, g1[0].black

        t.next_round()
        self.set_player_lost(t, a)
        self.set_player_lost(t, b)

        t.end_tournament()
        scoreboard = t.get_scoreboard()

        self.assertEqual(scoreboard[0][1], (3, 9, 0))
        self.assertEqual(scoreboard[1][1], (3, 3, 0))
        self.assertEqual(scoreboard[2][1], (2, 0, 3))
        self.assertEqual(scoreboard[3][1], (0, 0, 5))

    def test_points_2(self):
        players = get_dummy()[:4]

        t = SwissTournament('t6', players)
        t.next_round()

        # Testing replace results
        t.set_result(0, Result.Draw)
        t.set_result(1, Result.Black)
        t.set_result(0, Result.Playing)

        t.set_result(0, Result.Black)
        t.set_result(1, Result.Draw)

        g1 = t.active_round
        a, b = g1[0].white, g1[0].black

        t.next_round()
        self.set_player_win(t, a)
        self.set_player_lost(t, b)

        t.end_tournament()
        scoreboard = t.get_scoreboard()

        self.assertEqual(scoreboard[0][1], (3, 7, 0))
        self.assertEqual(scoreboard[1][1], (2, 6, 3))
        self.assertEqual(scoreboard[2][1], (2, 3, 2))
        self.assertEqual(scoreboard[3][1], (1, 3, 2))


if __name__ == '__main__':
    unittest.main()
