import itertools
import tkinter as tk

from src.gui.widgets.table_frame import TableFrame
from src.tournament.interactive_tournament import InteractiveTournament
from src.tournament.player import Player
from src.tournament.round import GameResult


class ContentFrame(tk.Frame):
    def __init__(self, parent, tournament: InteractiveTournament | None = None):
        super().__init__(parent)

        self.config(background="#BCBABE")

        self.table = TableFrame(self)
        self._is_table_packed = False

        self.update_tournament_view(tournament, page=-1)

    def update_tournament_view(self, tournament: InteractiveTournament | None, *, page: int):
        if tournament is None:
            self.table.data = []
            self.table.pack_forget()
            self._is_table_packed = False
            return
        elif not self._is_table_packed:
            self.table.pack(side=tk.TOP, fill=tk.X, padx=80, pady=40)
            self._is_table_packed = True

        updaters = [
            self._update_starting_list_view,
            *[lambda t, i2=i: self._update_round_view(t, i2) for i in range(tournament.round_count)],
            *([self._update_results_view] if tournament.is_finished() else []),
        ]

        # noinspection PyArgumentList
        updaters[page](tournament)

    def _update_starting_list_view(self, tournament: InteractiveTournament):
        headers = ['#', 'Gracz', 'Ranking']
        starting_list = zip(
            itertools.count(start=1),
            (self.__format_player(p) for p in tournament.players),
            (p.rating for p in tournament.players),
        )

        self.table.data = [headers, *starting_list]
        self.table.columns_weights = [1, 10, 5]

    def _update_round_view(self, tournament: InteractiveTournament, index: int):
        round_ = tournament.get_round(index)

        headers = ['#', 'Biały', 'Wynik', 'Czarny']
        data = zip(
            itertools.count(start=1),
            (self.__format_player_from_id(tournament, white) for white, _ in round_.pairs),
            (self.__format_game_result(result) for result in round_.results),
            (self.__format_player_from_id(tournament, black) for _, black in round_.pairs),
        )

        self.table.data = [headers, *data]
        self.table.columns_weights = [1, 7, 3, 7]

    def _update_results_view(self, tournament: InteractiveTournament):
        headers = ['#', 'Gracz', 'Punkty']
        scoreboard = tournament.get_scoreboard()
        scoreboard = zip(
            (pos for pos, player_id, points in scoreboard),
            (self.__format_player(player) for pos, player, points in scoreboard),
            (self.__format_points(points) for pos, player_id, points in scoreboard),
        )

        self.table.data = [headers, *scoreboard]
        self.table.columns_weights = [1, 7, 5]

    @staticmethod
    def __format_player(player: Player):
        return f'{player.name} {player.surname}'

    @classmethod
    def __format_player_from_id(cls, tournament: InteractiveTournament, player_id: int):
        return cls.__format_player(tournament.players[player_id])

    @staticmethod
    def __format_game_result(result: GameResult | None):
        if result is None:
            return ''

        return f'{result.points_a} - {result.points_b}'

    @staticmethod
    def __format_points(points: tuple[float, ...]):
        return ', '.join(map(str, points))
