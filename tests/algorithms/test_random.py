import unittest

from src.algorithms.random_tournament import RandomTournament
from src.algorithms.tournament import Result
from src.player import Player, Gender


def get_dummy():
    dummy_players = [
        Player('Adam', 'Nowak', Gender.Men, 1200),
        Player('Anna', 'Nowak', Gender.Women, 1100),
        Player('Maximum', 'Engine', Gender.Other, 3000),
        Player('Marcin', 'Nowak', Gender.Men, 800),
        Player('Maximum2', 'Engine2', Gender.Other, 3200),
        Player('Ryszard', 'Nowak', Gender.Men, 990),
    ]
    return dummy_players


class TestRandom(unittest.TestCase):
    def assert_round(self, players, round_, pairs):
        for game in round_:
            for i, pair in enumerate(pairs):
                if game.white in pair and game.black in pair:
                    del pairs[i]
                    break
            else:
                self.fail(f'Bad pair {game.white} with {game.black}')

    def test_no_error(self):
        players = get_dummy()[:6]
        t = RandomTournament(players)
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
        t = RandomTournament(players)
        t.set_result(0, Result.White)
        t.set_result(1, Result.Draw)
        t.set_result(2, Result.Draw)
        games = t.get_last_round()
        t.end_tournament()
        scoreboard = t.get_scoreboard()

        self.assertEqual(scoreboard[0][0], games[0].white)
        self.assertEqual(scoreboard[-1][0], games[0].black)



if __name__ == '__main__':
    unittest.main()
