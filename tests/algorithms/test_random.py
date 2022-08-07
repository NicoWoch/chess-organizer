import unittest

from src.algorithms.random_tournament import RandomTournament
from src.algorithms.tournament import Result
from src.player import Player, Gender


def get_dummy():
    dummy_players = [
        Player.create_player(name='Adam', surname='Nowak', gender=Gender.Men, rating=1200),
        Player.create_player(name='Anna', surname='Nowak', gender=Gender.Women, rating=1100),
        Player.create_player(name='Maximum', surname='Engine', gender=Gender.Other, rating=3000),
        Player.create_player(name='Marcin', surname='Nowak', gender=Gender.Men, rating=800),
        Player.create_player(name='Maximum2', surname='Engine2', gender=Gender.Other, rating=3200),
        Player.create_player(name='Ryszard', surname='Nowak', gender=Gender.Men, rating=990),
    ]
    return dummy_players


class TestRandom(unittest.TestCase):
    def assert_round(self, round_, pairs):
        for game in round_:
            for i, pair in enumerate(pairs):
                if game.white in pair and game.black in pair:
                    del pairs[i]
                    break
            else:
                self.fail(f'Bad pair {game.white} with {game.black}')

    def test_no_error(self):
        players = get_dummy()[:6]
        t = RandomTournament('t1', players)

        t.next_round()
        t.set_result(0, Result.White)
        t.set_result(1, Result.White)
        t.set_result(2, Result.White)

        for _ in range(2):
            t.next_round()
            t.set_result(0, Result.White)
            t.set_result(1, Result.White)
            t.set_result(2, Result.White)

    def test_scoreboard_and_points(self):
        players = get_dummy()[:6]
        t = RandomTournament('t2', players)
        t.next_round()
        t.set_result(0, Result.White)
        t.set_result(1, Result.Draw)
        t.set_result(2, Result.Draw)

        games = t.active_round
        t.next_round()
        scoreboard = t.get_scoreboard()

        self.assertEqual(scoreboard[0][0], games[0].white)
        self.assertEqual(scoreboard[-1][0], games[0].black)



if __name__ == '__main__':
    unittest.main()
