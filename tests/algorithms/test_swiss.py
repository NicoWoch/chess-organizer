import functools
import math
import random
import unittest
from typing import Callable

from src.algorithms.constants import Result
from src.algorithms.swiss_tournament import SwissTournament
from src.dummy_generator import get_random_players

RNG = random.Random(29)
REPEAT_TIMES_MULTIPLIER = 1


def repeat_random_test(times: int):
    def decorator(func: Callable):
        @functools.wraps(func)
        def inner(self):
            for _ in range(times * REPEAT_TIMES_MULTIPLIER):
                self.setUp()
                func(self)

        return inner

    return decorator


class TestSwiss(unittest.TestCase):
    def setUp(self):
        self.tournament = SwissTournament('tournament')

    def __add_dummy_players(self, count: int):
        while True:
            players = sorted(get_random_players(count, rng=RNG), key=lambda p: p.rating, reverse=True)

            if len(set(p.rating for p in players)) != len([p.rating for p in players]):
                continue

            if len(set(players)) != len(players):
                continue

            break

        self.tournament.add_players(players)

    def __assert_next_round(self, round_by_names: list[tuple[int, int]], pauses: set[int]):
        self.tournament.next_round()

        self.assertEqual(len(self.tournament.last_round), len(round_by_names), msg='Bad length of pairs')

        for i, expected_pair in enumerate(round_by_names):
            true_white_id = self.tournament.players.index(self.tournament.last_round[i].white)
            true_black_id = self.tournament.players.index(self.tournament.last_round[i].black)

            self.assertEqual((true_white_id, true_black_id), expected_pair, msg=f'Bad pair on table {i}')

        self.assertEqual(len(self.tournament.get_pause()), len(pauses), msg='Bad length of pause')
        self.assertEqual(set(self.tournament.players.index(p) for p in self.tournament.get_pause()), pauses, msg='Bad pause players')

    def test_no_error_to_40_players(self):
        for no_players in range(5, 40):
            prefered_rounds_count = math.ceil(math.log2(no_players))
            games_in_round = no_players // 2

            self.tournament = SwissTournament(f'tournament {no_players}')
            self.__add_dummy_players(no_players)

            pause = set()
            for round_no in range(prefered_rounds_count):
                error_message = f'Fail while testing tournament with {no_players} players on {round_no + 1} round'
                self.tournament.next_round()

                self.assertEqual(len(self.tournament.last_round), games_in_round, msg=error_message)

                if no_players % 2 == 0:
                    self.assertEqual(len(self.tournament.get_pause()), 0, msg=error_message)
                else:
                    self.assertEqual(len(self.tournament.get_pause()), 1, msg=error_message)
                    self.assertNotIn(self.tournament.get_pause()[0], pause, msg=error_message)
                    pause.add(self.tournament.get_pause()[0])

                for i in range(games_in_round):
                    self.tournament.set_result(i, RNG.choice([Result.White, Result.Draw, Result.Black]))

    @repeat_random_test(3)
    def test_pairing_first_round_1(self):
        self.__add_dummy_players(4)

        self.__assert_next_round([
            (0, 2),
            (1, 3),
        ], set())

    @repeat_random_test(3)
    def test_pairing_first_round_2(self):
        self.__add_dummy_players(7)

        self.__assert_next_round([
            (0, 3),
            (1, 4),
            (2, 5),
        ], {6})

    def __set_next_round_results(self, results: list[Result]):
        self.tournament.next_round()

        for i, result in enumerate(results):
            self.tournament.set_result(i, result)

    @repeat_random_test(5)
    def test_pairing_second_round_1(self):
        self.__add_dummy_players(7)

        self.__set_next_round_results([Result.Black, Result.White, Result.White])

        self.__assert_next_round([
            (3, 1),
            (6, 2),
            (4, 0),
        ], {5})

    @repeat_random_test(5)
    def test_pairing_second_round_2(self):
        self.__add_dummy_players(8)

        self.__set_next_round_results([Result.Black, Result.White, Result.Draw, Result.Black])

        self.__assert_next_round([
            (4, 1),
            (7, 2),
            (6, 3),
            (5, 0),
        ], set())


    @repeat_random_test(5)
    def test_pairing_second_round_3(self):
        self.__add_dummy_players(8)

        self.__set_next_round_results([Result.Black, Result.Draw, Result.Draw, Result.Draw])

        self.__assert_next_round([
            (4, 1),
            (5, 2),
            (6, 3),
            (7, 0),
        ], set())

    @repeat_random_test(5)
    def test_pairing_second_round_4(self):
        self.__add_dummy_players(11)

        self.__set_next_round_results([Result.White, Result.White, Result.Draw, Result.White, Result.Draw])

        self.__assert_next_round([
            (1, 0),
            (10, 3),
            (9, 2),
            (7, 4),
            (6, 5),
        ], {8})

    @repeat_random_test(10)
    def test_pairing_third_round_1(self):
        self.__add_dummy_players(8)

        self.__set_next_round_results([Result.Black, Result.Draw, Result.Draw, Result.Draw])
        self.__set_next_round_results([Result.Draw, Result.Draw, Result.White, Result.Black])

        self.__assert_next_round([
            (6, 4),
            (1, 0),
            (2, 7),
            (3, 5),
        ], set())

    @repeat_random_test(5)
    def test_pairing_third_round_2(self):
        self.__add_dummy_players(11)

        self.__set_next_round_results([Result.White, Result.White, Result.Draw, Result.White, Result.Draw])
        self.__set_next_round_results([Result.Black, Result.Black, Result.Draw, Result.Draw, Result.Black])

        self.__assert_next_round([
            (3, 0),
            (2, 1),
            (4, 10),
            (5, 7),
            (8, 9),
        ], {6})

    @repeat_random_test(5)
    def test_pairing_fourth_round_1(self):
        self.__add_dummy_players(11)

        self.__set_next_round_results([Result.White, Result.White, Result.Draw, Result.White, Result.Draw])
        self.__set_next_round_results([Result.Black, Result.Black, Result.Draw, Result.Draw, Result.Black])
        self.__set_next_round_results([Result.White, Result.Black, Result.Black, Result.Draw, Result.White])

        self.__assert_next_round([
            (1, 3),
            (0, 8),
            (5, 10),
            (7, 6),
            (4, 2),
        ], {9})



if __name__ == '__main__':
    unittest.main()
