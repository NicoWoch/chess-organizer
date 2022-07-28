import unittest

from src.algorithms.swiss.swiss_tournament import SwissTournament
from src.player import Player, Gender


def get_dummy():
    dummy_players = [
        Player('Adam', 'Nowak', Gender.Men, 1200),
        Player('Anna', 'Nowak', Gender.Women, 1100),
        Player('Maximum', 'Engine', Gender.Other, 3000),
        Player('Marcin', 'Nowak', Gender.Men, 800),
    ]
    return dummy_players


class TestSwiss(unittest.TestCase):
    def assert_round(self, players, round_, pairs):
        for game in round_:
            for i, pair in enumerate(pairs):
                if game.white in pair and game.black in pair:
                    del pairs[i]
                    break
            else:
                self.fail(f'Bad pair {game.white} with {game.black}')

    def test_pairing_1(self):
        players = get_dummy()[:4]
        t = SwissTournament(players)
        t.start_round()
        t.set_win(players[0])
        t.set_win(players[1])
        t.finish_round()
        t.start_round()

        self.assert_round(players, t.rounds[-1], [
            (players[0], players[2]),
            (players[1], players[3])
        ])

    def test_no_error(self):
        players = get_dummy()[:4]
        t = SwissTournament(players)
        for _ in range(2):
            t.start_round()
            t.set_win(t.rounds[-1][0].white)
            t.set_win(t.rounds[-1][1].white)
            t.finish_round()


if __name__ == '__main__':
    unittest.main()
