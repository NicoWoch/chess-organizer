import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from src.algorithms.constants import Result, Round, Points
from src.algorithms.elo import elo_rating
from src.algorithms.errors import TournamentNotRunningError, TournamentStartedError, PlayerExistsError, TournamentEndedError, RoundNotEnded
from src.config import Config
from src.player import Player

Pairing = tuple[Round, list[Player]]


class Tournament(ABC):
    def __init__(self, name: str):
        self.name = name
        self.started_date: Optional[datetime] = None

        self._players: list[Player] = []
        self._points: list[Points] = []
        self._opponents: list[dict[Result, list[int]]] = []

        self._rounds: list[Round] = []
        self._pause: list[list[Player]] = []

        self.is_started = False
        self.is_ended = False

        self.ratings_before: list[int] = []
        self.ratings_after: list[int] = []

    @property
    def players(self) -> list[Player]:
        return self._players.copy()

    @property
    def players_count(self) -> int:
        return len(self._players)

    @property
    def is_running(self):
        return self.is_started and not self.is_ended

    def _assert_tournament_running(self):
        if not self.is_running:
            raise TournamentNotRunningError

    def _assert_tournament_not_started(self):
        if self.is_started:
            raise TournamentStartedError

    def add_player(self, player: Player):
        self._assert_tournament_not_started()

        if player in self._players:
            raise PlayerExistsError

        self._players.append(player)
        self._points.append(self._get_default_points())
        self._opponents.append({Result.White: [], Result.Draw: [], Result.Black: []})
        self.ratings_before.append(player.rating)

    def add_players(self, players: list[Player]):
        for player in players:
            self.add_player(player)

    def remove_player(self, player: Player):
        self._assert_tournament_not_started()

        player_id = self._players.index(player)
        del self._players[player_id], self._points[player_id], self._opponents[player_id]
        del self.ratings_before[player_id]

    def get_points(self, player_id: int):
        return self._points[player_id]

    def get_opponents(self, player_id: int):
        return self._opponents[player_id]

    @property
    def round_count(self) -> int:
        return len(self._rounds)

    @property
    def last_round(self) -> Round:
        return self._rounds[-1]

    def get_round(self, round_id) -> Round:
        return self._rounds[round_id]

    def get_pause(self, round_id=-1) -> list[Player]:
        return self._pause[round_id]

    def get_scoreboard(self) -> list[tuple[int, Player, Points]]:
        scoreboard = []

        pos = 0
        last_score = None
        for player, score in sorted(zip(self._players, self._points), key=lambda x: x[1], reverse=True):
            if last_score is None or last_score != score:
                pos += 1

            scoreboard.append((pos, player, score))
            last_score = score

        return scoreboard

    def set_result(self, table_id: int, new_result: Result):
        self._assert_tournament_running()

        game = self.last_round[table_id]

        # Clear old result
        self.__change_points_by_result(game.white, game.black, game.result, -1)
        self.__change_points_by_result(game.black, game.white, game.result.opposite(), -1)

        # Apply new result
        self.__change_points_by_result(game.white, game.black, new_result, 1)
        self.__change_points_by_result(game.black, game.white, new_result.opposite(), 1)
        game.result = new_result

    def __change_points_by_result(self, player: Player, opponent: Player, result: Result, points_mul: int):
        if points_mul not in (-1, 1):
            raise ValueError(f'Bad points_mul. {points_mul} should be -1 or 1')

        player_id = self.players.index(player)
        opponent_id = self.players.index(opponent)

        self._points[player_id].big_points += result.get_points() * points_mul

        if result != Result.Playing:
            if points_mul == 1:
                self._opponents[player_id][result].append(opponent_id)
            elif points_mul == -1:
                self._opponents[player_id][result].remove(opponent_id)

    def next_round(self):
        if not self.is_started:
            self.__start_round(1)
            self.started_date = datetime.now().astimezone()
            self.is_started = True
            self.__trigger_playing_to_players()
            return

        if self.is_ended:
            raise TournamentEndedError

        logging.debug(f'Tournament "{self.name}": Next round ({self.round_count + 1})')

        self.__end_round()
        self.__start_round(self.round_count + 1)

    def __trigger_playing_to_players(self):
        for player in self._players:
            player.trigger_playing()

    def __start_round(self, round_no: int):
        pairs, pauses = self._pair_round(round_no)

        pause_points = Config.PAUSE_POINTS

        for pause in pauses:
            pause_id = self._players.index(pause)
            self._points[pause_id].big_points += pause_points

        self._rounds.append(pairs)
        self._pause.append(pauses)

    def __end_round(self):
        if not self.has_round_ended():
            not_ended_count = sum(game.result == Result.Playing for game in self.last_round)
            raise RoundNotEnded(not_ended_count)

        self._update_points()

    def has_round_ended(self) -> bool:
        return all(game.result != Result.Playing for game in self.last_round)

    def end_tournament(self):
        self._assert_tournament_running()

        logging.debug(f'Tournament "{self.name}": Ending tournament after {self.round_count} rounds')

        self.__end_round()
        self.__calculate_new_ratings()
        self.is_ended = True

    def __calculate_new_ratings(self):
        ratings = self.ratings_before.copy()

        for games in self._rounds:
            for game in games:
                white_id, black_id = self._players.index(game.white), self._players.index(game.black)

                if game.result == Result.Playing:
                    raise Exception('Some games not ended yet (when calculating new ratings)')

                points = game.result.get_points()

                ratings[white_id], ratings[black_id] = elo_rating(ratings[white_id], ratings[black_id], points)

        self.ratings_after = ratings

    @abstractmethod
    def _get_default_points(self) -> Points: ...

    @abstractmethod
    def _pair_round(self, round_no: int) -> Pairing: ...

    @abstractmethod
    def _update_points(self): ...
