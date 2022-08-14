import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from src.algorithms.elo import elo_rating
from src.algorithms.game import Result, Round
from src.player import Player


class Tournament(ABC):
    def __init__(self, name: str, players: list[Player]):
        self.name = name
        self.started_date: Optional[datetime] = None

        self._players: list[Player] = []
        self._points: list[tuple] = []
        self._stats: list[dict[Result, list[int]]] = []

        self._rounds: list[Round] = []
        self._pausing_players: list[list[Player]] = []

        self._is_started = False
        self._is_ended = False

        self.old_ratings: list[int] = []

        for player in players:
            self.add_player(player)

    @property
    def players(self) -> list[Player]:
        return self._players.copy()

    def add_player(self, player: Player):
        if self._is_started:
            raise Exception('Cannot add player when tournament is running')

        if player in self._players:
            logging.warning(f'Player "{player}" is already added')
            return

        logging.debug(f'Tournament "{self.name}": Adding player "{player}"')

        self._players.append(player)
        self._points.append(self._get_default_points())
        self._stats.append({Result.White: [], Result.Draw: [], Result.Black: []})
        self.old_ratings.append(player.rating)

    def remove_player(self, player: Player):
        if self._is_started:
            raise Exception('Cannot remove player when tournament is running')

        player_id = self._players.index(player)
        del self._players[player_id]
        del self._points[player_id]
        del self._stats[player_id]
        del self.old_ratings[player_id]

    def get_player_id(self, player: Player):
        return self._players.index(player)

    def get_points(self, player_id: int):
        return self._points[player_id]

    def get_stats(self, player_id: int):
        return self._stats[player_id]

    def is_started(self):
        return self._is_started

    def is_ended(self):
        return self._is_ended

    @property
    def round_count(self) -> int:
        return len(self._rounds)

    @property
    def active_round_id(self) -> Optional[int]:
        if not self._is_started or self._is_ended:
            return None

        return len(self._rounds) - 1

    @property
    def active_round(self) -> Optional[Round]:
        if not self._is_started or self._is_ended:
            return None

        return self._rounds[-1]

    def get_round(self, round_id) -> Round:
        return self._rounds[round_id]

    def get_waiting_players(self, round_id=-1) -> list[Player]:
        return self._pausing_players[round_id]

    def has_round_ended(self) -> bool:
        if not self.is_started():
            return True

        return all(game.result != Result.Playing for game in self.active_round)

    def get_scoreboard(self) -> list[tuple[Player, tuple]]:
        return sorted(zip(self._players, self._points), key=lambda x: x[1], reverse=True)

    def get_scoreboard_ids(self) -> list[int]:
        return [self.get_player_id(player) for player, points in self.get_scoreboard()]

    def get_scoreboard_str(self, main_sep=' ', points_sep=', ') -> list[str]:
        return [str(player) + main_sep + points_sep.join(points) for player, points in self.get_scoreboard()]

    def set_result(self, table_id: int, new_result: Result):
        if not self._is_started:
            raise Exception('Tournament not started')

        if self._is_ended:
            raise Exception('Tournament already ended')

        game = self.active_round[table_id]

        logging.debug(f'Tournament "{self.name}": Setting result {new_result} for table_id {table_id} with result {game.result}')

        # Clear old result
        self.__change_player_by_result(game.white, game.black, game.result, -1)
        self.__change_player_by_result(game.black, game.white, game.result.opposite(), -1)

        # Apply new result
        self.__change_player_by_result(game.white, game.black, new_result, 1)
        self.__change_player_by_result(game.black, game.white, new_result.opposite(), 1)
        game.result = new_result

    def __change_player_by_result(self, player: Player, opponent: Player, result: Result, points_mul: int):
        if points_mul not in (-1, 1):
            raise ValueError(f'Bad points_mul. {points_mul} should be 1 or -1')

        win, draw, lost = self._get_win_draw_lost_points()

        if result == Result.White:
            points_change = win
        elif result == Result.Black:
            points_change = lost
        elif result == Result.Draw:
            points_change = draw
        else:
            points_change = 0

        points_change *= points_mul
        player_id = self.players.index(player)
        opponent_id = self.players.index(opponent)

        self._points[player_id] = (
            self._points[player_id][0] + points_change,
            *self._points[player_id][1:]
        )

        if result != Result.Playing:
            if points_mul == 1:
                self._stats[player_id][result].append(opponent_id)
            elif points_mul == -1:
                self._stats[player_id][result].remove(opponent_id)

    def next_round(self):
        if not self._is_started:
            self._start_round()
            self.started_date = datetime.now().astimezone()
            self._is_started = True
            return

        if self._is_ended:
            raise Exception('Tournament arleady ended')

        logging.debug(f'Tournament "{self.name}": Next round')

        self._end_round()
        self._start_round()

    def end_tournament(self):
        if not self._is_started:
            raise Exception('Tournament not started yet')

        if self._is_ended:
            raise Exception('Tournament arleady ended')

        logging.debug(f'Tournament "{self.name}": Ending tournament')

        self._end_round()
        self._is_ended = True

    def _start_round(self):
        pairs, pauses = self._pair_round()

        pause_points, _, _ = self._get_win_draw_lost_points()

        for pause in pauses:
            pause_id = self._players.index(pause)
            self._points[pause_id] = (
                self._points[pause_id][0] + pause_points,
                self._points[pause_id][1], self._points[pause_id][2]
            )

        self._rounds.append(pairs)
        self._pausing_players.append(pauses)

        self._trigger_playing_to_players()

    def _end_round(self):
        if not self.has_round_ended():
            not_ended_count = len([g for g in self.active_round if g.result == Result.Playing])
            raise Exception(f'Round not ended yet on {not_ended_count} tables')

        self._update_points()

    def _trigger_playing_to_players(self):
        for player in self._players:
            player.trigger_playing()

    @property
    def new_ratings(self) -> list[int]:
        ratings = self.old_ratings.copy()

        for games in self._rounds:
            for game in games:
                white_id, black_id = self._players.index(game.white), self._players.index(game.black)

                if game.result == Result.White:
                    points = 1
                elif game.result == Result.Draw:
                    points = 0.5
                elif game.result == Result.Black:
                    points = 0
                else:
                    raise Exception('Some game not ended yet (when calculating new ratings)')

                ratings[white_id], ratings[black_id] = elo_rating(ratings[white_id], ratings[black_id], points)

        return ratings

    @abstractmethod
    def _get_default_points(self) -> tuple: ...

    @abstractmethod
    def _get_win_draw_lost_points(self) -> tuple[int, int, int]: ...

    @abstractmethod
    def _pair_round(self) -> tuple[Round, list[Player]]: ...

    @abstractmethod
    def _update_points(self): ...
