import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Iterable, Iterator

from src.algorithms.constants import Result, Points, Game
from src.algorithms.elo import elo_rating
from src.algorithms.errors import TournamentNotRunningError, TournamentStartedError
from src.algorithms.errors import PlayerExistsError, TournamentEndedError, RoundNotEnded
from src.config import Config
from src.player import Player

type Pairs = tuple[tuple[int, int], ...]


class Pairer(ABC):
    tournament: 'Tournament'

    @abstractmethod
    def get_starting_points(self) -> Points: ...

    @abstractmethod
    def calculate_small_points(self, points: list[Points], till_round: int = None) -> Iterable[Points]: ...

    @abstractmethod
    def pair_next_round(self) -> Pairs: ...


class Tournament:
    def __init__(self, name: str, pairer: Pairer):
        self.name = name
        self.started_date: Optional[datetime] = None

        self._pairer = pairer
        self._pairer.tournament = self

        self._players: tuple[Player, ...] = ()
        self._rounds: list[tuple[Game, ...]] = []

        self._ratings_at_start: tuple[int, ...] = ()
        self._ratings_at_end: tuple[int, ...] = ()
        self._is_finished = False

    @property
    def players(self) -> tuple[Player, ...]:
        return self._players

    @property
    def players_count(self) -> int:
        return len(self._players)

    @property
    def is_started(self):
        return len(self._rounds) != 0

    @property
    def is_finished(self):
        return self._is_finished

    @property
    def is_running(self):
        return self.is_started and not self.is_finished

    @staticmethod
    def __player_order_key(player: Player) -> int:
        return -player.rating

    def add_player(self, player: Player):
        self._assert_not_started()

        if player in self._players:
            raise PlayerExistsError(player)

        self._players = tuple(sorted(self._players + (player,), key=self.__player_order_key))

    def add_players(self, players: Iterable[Player]):
        for player in players:
            self.add_player(player)

    def remove_player(self, player: Player):
        self._assert_not_started()

        player_id = self._players.index(player)
        self._players = self._players[:player_id] + self._players[player_id + 1:]

    def calculate_points(self, *, till_round: int | None = None) -> tuple[Points, ...]:
        points = [self._pairer.get_starting_points() for _ in range(self.players_count)]

        for game in self.iterate_over_all_games(till_round):
            points[game.white].base_big += game.result.get_points()
            points[game.black].base_big += game.result.opposite().get_points()

        for i in range(len(self._rounds)):
            for player_id in self.calculate_pause_indices(i):
                points[player_id].pause += Config.PAUSE_POINTS

        return tuple(self._pairer.calculate_small_points(points, till_round))

    @property
    def rounds(self) -> tuple[tuple[Game, ...], ...]:
        return tuple(self._rounds)

    @property
    def last_round(self) -> tuple[Game, ...]:
        return self._rounds[-1]

    def calculate_pause_indices(self, round_id: int = -1) -> tuple[int, ...]:
        assert round_id == -1 or 0 <= round_id < len(self._rounds), f'Round index is out of bounds ({round_id=})'

        pause = list(range(self.players_count))

        for game in self._rounds[round_id]:
            pause.remove(game.white)
            pause.remove(game.black)

        return tuple(pause)

    def calculate_pause(self, round_id: int = -1) -> tuple[Player, ...]:
        return tuple(
            self._players[index] for index in self.calculate_pause_indices(round_id)
        )

    def create_scoreboard(self, *, till_round: int | None = None) -> list[tuple[int, Player, Points]]:
        scoreboard = []

        pos = 1
        last_score = None
        sorted_scores: list[tuple[Player, Points]] = sorted(
            zip(self._players, self.calculate_points(till_round=till_round)),
            key=lambda x: x[1], reverse=True
        )

        for i, (player, score) in enumerate(sorted_scores, start=1):
            if last_score is None or last_score != score:
                pos = i
                last_score = score

            scoreboard.append((pos, player, score))

        return scoreboard

    def set_result(self, table_id: int, new_result: Result):
        self._assert_running()
        self.last_round[table_id].result = new_result

    def next_round(self):
        if not self.is_started:
            self.started_date = datetime.now()
            self._ratings_at_start = tuple(player.rating for player in self._players)
            self.__trigger_playing_to_players()
            self.__start_round()
            return

        if self.is_finished:
            raise TournamentEndedError()

        logging.debug(f'Tournament "{self.name}": Next round ({len(self._rounds) + 1})')

        self.__end_round()
        self.__start_round()

    def remove_last_round(self):
        self._assert_running()
        self._rounds.pop()

        if not self.is_started:
            self.started_date = None
            self._ratings_at_start = ()

    def __trigger_playing_to_players(self):
        for player in self._players:
            player.trigger_playing()

    def __start_round(self):
        self._rounds.append(tuple(
            Game(white, black) for white, black in self._pairer.pair_next_round()
        ))

    def __end_round(self):
        if not self.are_all_games_finished():
            not_ended_count = sum(game.result == Result.Playing for game in self.last_round)
            raise RoundNotEnded(not_ended_count)

    def are_all_games_finished(self) -> bool:
        return all(game.result != Result.Playing for game in self.last_round)

    def end_tournament(self):
        self._assert_running()

        self.__end_round()
        self.__calculate_new_ratings()
        self._is_finished = True

        logging.debug(f'Tournament "{self.name}": Finished tournament after {len(self._rounds)} rounds')

    def __calculate_new_ratings(self):
        ratings = list(self._ratings_at_start)

        for games in self._rounds:
            for game in games:
                white_id, black_id = self._players.index(game.white), self._players.index(game.black)

                if game.result == Result.Playing:
                    raise Exception('Some games not ended yet (when calculating new ratings)')

                points = game.result.get_points()

                ratings[white_id], ratings[black_id] = elo_rating(ratings[white_id], ratings[black_id], points)

        self._ratings_at_end = tuple(ratings)

    @property
    def ratings_at_start(self) -> tuple[int, ...]:
        assert self.is_started, 'Tournament has to be started to get ratings at start'
        return self._ratings_at_start

    @property
    def ratings_at_end(self) -> tuple[int, ...]:
        assert self.is_finished, 'Tournament has to be finished to get ratings at end'
        return self._ratings_at_end

    def iterate_over_all_games(self, till_round: int | None = None) -> Iterator[Game]:
        assert till_round is None or 0 <= till_round < len(self._rounds), f'Round index is out of bounds ({till_round=})'

        rounds = self._rounds if till_round is None else self._rounds[:till_round]

        for round_games in rounds:
            yield from round_games

    def _assert_running(self):
        if not self.is_running:
            raise TournamentNotRunningError()

    def _assert_not_started(self):
        if self.is_started:
            raise TournamentStartedError()
