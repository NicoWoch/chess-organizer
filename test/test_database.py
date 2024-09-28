import os.path
import unittest
from typing import Any

from src import database
from src.tournament.interactive_tournament import InteractiveTournament, TournamentData
from src.tournament.pairing.dutch_pairer import DutchPairer
from src.tournament.player import Player
from src.tournament.round import GameResult
from src.tournament.scoring.buchholz_scorer import BuchholzScorer
from src.tournament.scoring.points_scorer import PointsScorer
from src.tournament.tournament import TournamentSettings

DATABASE_TMP_PATH = 'db.tmp.json'


class TestDatabase(unittest.TestCase):
    def test_file_creation(self):
        if os.path.isfile(DATABASE_TMP_PATH):
            os.remove(DATABASE_TMP_PATH)

        db = database.Database(DATABASE_TMP_PATH)
        db.read()

        self.assertTrue(os.path.isfile(DATABASE_TMP_PATH), 'Database does not created a db file')

    def __test_read_write(self, value: Any):
        db = database.Database(DATABASE_TMP_PATH)
        db.write(value)
        red = db.read()

        self.assertEqual(value, red)
        self.assertEqual(type(value), type(red))
        self.assertEqual(dir(value), dir(red))

    def __test_read_write_manual(self, value: Any):
        db = database.Database(DATABASE_TMP_PATH)
        db.write(value)
        red = db.read()
        return value, red

    def test_simple_types_1(self):
        self.__test_read_write(5)

    def test_simple_types_2(self):
        self.__test_read_write('hello world')

    def test_simple_types_3(self):
        self.__test_read_write([1, 4, 2, 3])

    def test_simple_types_4(self):
        self.__test_read_write({'x': 2, 'y': 3})

    def test_nested_types(self):
        self.__test_read_write({'x': [[[[2]], 1], [3]], 'y': [[[{'z': [5]}]], [], 2]})

    def test_player(self):
        self.__test_read_write(Player('Adam', rating=2000))
        self.__test_read_write([Player('Adam'), ])

    def test_nested_player(self):
        self.__test_read_write({'x': Player('X', rating=1500, hash_id=2),
                                'y': [1, {'1': Player('Alan')}, Player('X', rating=1500, hash_id=1)]})

    def test_game_result(self):
        self.__test_read_write(
            [GameResult.WIN, GameResult.LOSE, GameResult.DRAW, GameResult.PLAYER_A_NOT_SHOWED_IN_TIME])

    def test_scorer(self):
        data, red = self.__test_read_write_manual([
            TournamentSettings(scorer=PointsScorer()),
            TournamentSettings(scorer=BuchholzScorer()),
        ])

        self.assertEqual(list, type(red))
        self.assertEqual(2, len(red))
        self.assertEqual(PointsScorer, red[0].scorer.__class__)
        self.assertEqual(BuchholzScorer, red[1].scorer.__class__)

    @staticmethod
    def __create_sample_it(*, players=None, rounds=()):
        tournament = InteractiveTournament(TournamentData('test', 'some_category'))

        if players is None:
            tournament.add_player(Player('Anna', rating=2000))
            tournament.add_player(Player('Barbara', rating=1200))
            tournament.add_player(Player('Cezary', rating=1500))
            tournament.add_player(Player('Danuta'))
        else:
            for player in players:
                tournament.add_player(player)

        for pairs, results in rounds:
            tournament.next_round(pairs)

            for table, result in enumerate(results):
                tournament.set_result(table, result)

        return tournament

    def __compare_interactive_tournament(self, expected: InteractiveTournament, actual: InteractiveTournament):
        self.assertEqual(InteractiveTournament, type(actual))
        self.assertEqual(expected.data, actual.data)
        self.assertEqual(expected.players, actual.players)
        self.assertEqual(expected.round_count, actual.round_count)

        for i in range(expected.round_count):
            self.assertEqual(expected.get_round(i).pairs, actual.get_round(i).pairs)
            self.assertEqual(expected.get_round(i).results, actual.get_round(i).results)
            self.assertEqual(expected.get_stats(i), actual.get_stats(i))

        if expected.round_count > 0:
            self.assertEqual(expected.get_scores(), actual.get_scores())
            self.assertEqual(expected.stats, actual.stats)
            self.assertEqual(expected.get_id_scoreboard(), actual.get_id_scoreboard())
            self.assertEqual(expected.get_player_scoreboard(), actual.get_player_scoreboard())

        self.assertEqual(expected.state, actual.state)
        self.assertEqual(expected.get_settings().elo_k_value, actual.get_settings().elo_k_value)
        self.assertEqual(expected.get_settings().scorer.__class__, actual.get_settings().scorer.__class__)
        self.assertEqual(expected.is_running(), actual.is_running())
        self.assertEqual(expected.is_finished(), actual.is_finished())

    def test_interactive_tournament_1(self):
        it = self.__create_sample_it(rounds=[
            (((0, 2), (1, 3)), (GameResult.WIN, GameResult.DRAW)),
            (((0, 3), (1, 2)), (GameResult.LOSE, GameResult.DRAW)),
        ])

        self.__compare_interactive_tournament(*self.__test_read_write_manual(it))

    def test_interactive_tournament_2(self):
        it = self.__create_sample_it(rounds=[
            (DutchPairer(), (GameResult.PLAYER_B_NOT_SHOWED_IN_TIME, GameResult.WIN)),
            (DutchPairer(), (GameResult.WIN, GameResult.LOSE)),
            (DutchPairer(), (GameResult.DRAW, GameResult.PLAYER_A_NOT_SHOWED_IN_TIME)),
        ])

        it.finish()

        self.__compare_interactive_tournament(*self.__test_read_write_manual(it))

    def test_interactive_tournament_3(self):
        it = self.__create_sample_it()

        self.__compare_interactive_tournament(*self.__test_read_write_manual(it))

    def test_sample_all_db_data(self):
        players = [
            Player('Adam', rating=2000),
            Player('Barbara', rating=1200),
            Player('Cezary', rating=1500),
            Player('Damian', rating=1700),
            Player('Elżbieta', rating=1800),
            Player('Franek', rating=1500),
            Player('Grażyna', rating=1300),
        ]

        db = {
            'players': players,
            'tournaments': [
                self.__create_sample_it(players=players[:5]),
                self.__create_sample_it(players=players),
                self.__create_sample_it(players=players[:5], rounds=(
                    (DutchPairer(), (GameResult.WIN,) * 2),
                    (DutchPairer(), (GameResult.WIN,) * 2),
                    (DutchPairer(), (GameResult.WIN,)),
                )),
                self.__create_sample_it(players=players[:7], rounds=(
                    (DutchPairer(), ()),
                )),
                self.__create_sample_it(players=players[:7], rounds=(
                    (DutchPairer(), (GameResult.WIN,) * 3),
                    (DutchPairer(), (GameResult.WIN,) * 3),
                    (DutchPairer(), (GameResult.WIN,) * 3),
                    (DutchPairer(), (GameResult.LOSE, GameResult.DRAW)),
                )),
            ],
            'settings': {
                'volume': -100
            }
        }

        _, red_db = self.__test_read_write_manual(db)

        self.assertEqual(db['players'], red_db['players'])
        self.assertEqual(db['settings'], red_db['settings'])

        for it, red_it in zip(db['tournaments'], red_db['tournaments']):
            self.__compare_interactive_tournament(it, red_it)


if __name__ == '__main__':
    unittest.main()
