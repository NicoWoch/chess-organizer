import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, List, Dict

from src.player import Player


class Result(Enum):
    White = '2 - 0'
    Black = '0 - 2'
    Draw = '1 - 1'
    Playing = '-'

    def opposite(self):
        if self == Result.White:
            return Result.Black
        elif self == Result.Black:
            return Result.White
        else:
            return self


@dataclass
class Game:
    white: Player
    black: Player
    result: Result


Round = List[Game]


class Tournament(ABC):
    def __init__(self, name: str, players: List[Player]):
        self.name = name

        self._players: List[Player] = []
        self._points: List[tuple] = []
        self._stats: List[Dict[Result, List[int]]] = []

        self._rounds: List[Round] = []
        self._pausing_players: List[List[Player]] = []

        self._is_started = False
        self._is_ended = False

        for player in players:
            self.add_player(player)

    @property
    def players(self) -> List[Player]:
        return self._players.copy()

    def add_player(self, player: Player):
        if self._is_started:
            raise Exception('Cannot add player when tournament is running')

        if player in self._players:
            logging.warning('Player is already added')
            return

        self._players.append(player)
        self._points.append(self._get_default_points())
        self._stats.append({Result.White: [], Result.Draw: [], Result.Black: []})

    def is_started(self):
        return self._is_started

    def is_ended(self):
        return self._is_ended

    @property
    def round_count(self) -> int:
        return len(self._rounds)

    @property
    def active_round(self) -> Round:
        return self._rounds[-1] if len(self._rounds) > 0 else None

    def get_round(self, round_id) -> Round:
        return self._rounds[round_id]

    def get_waiting_players(self, round_id=-1) -> List[Player]:
        return self._pausing_players[round_id]

    def has_round_ended(self) -> bool:
        return all(game.result != Result.Playing for game in self.active_round)

    def get_scoreboard(self) -> List[Tuple[Player, tuple]]:
        return sorted(zip(self._players, self._points), key=lambda x: x[1], reverse=True)

    def get_scoreboard_str(self, main_sep=' ', points_sep=', ') -> List[str]:
        return [str(player) + main_sep + points_sep.join(points) for player, points in self.get_scoreboard()]

    def set_result(self, table_id: int, new_result: Result):
        if not self._is_started:
            raise Exception('Tournament not started')

        game = self.active_round[table_id]

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
            self._is_started = True
            return

        if self._is_ended:
            raise Exception('Tournament arleady ended')

        self._end_round()
        self._start_round()

    def end_tournament(self):
        if not self._is_started:
            raise Exception('Tournament not started yet')

        if self._is_ended:
            raise Exception('Tournament arleady ended')

        self._end_round()
        self._update_ratings()
        self._is_ended = True

    def _start_round(self):
        pairs, pause = self._pair_round()
        self._rounds.append(pairs)
        self._pausing_players.append(pause)

    def _end_round(self):
        if not self.has_round_ended():
            not_ended_count = len([g for g in self.active_round if g.result == Result.Playing])
            raise Exception(f'Round not ended yet on {not_ended_count} tables')

        self._update_points()

    def _update_ratings(self):
        logging.info('Updating ratings comming soon')
        pass

    @abstractmethod
    def _get_default_points(self) -> tuple: ...

    @abstractmethod
    def _get_win_draw_lost_points(self) -> tuple[int, int, int]: ...

    @abstractmethod
    def _pair_round(self) -> Tuple[Round, List[Player]]: ...

    @abstractmethod
    def _update_points(self): ...
