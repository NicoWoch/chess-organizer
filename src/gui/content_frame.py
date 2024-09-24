import itertools
import tkinter as tk

from src.gui.widgets.player_with_rating_field import PlayerWithRatingField
from src.gui.widgets.resizing_widgets import ResizingLabel
from src.gui.widgets.table_frame import TableFrame
from src.tournament.interactive_tournament import InteractiveTournament
from src.tournament.player import Player
from src.tournament.round import GameResult


class ContentFrame(tk.Frame):
    def __init__(self, parent, tournament: InteractiveTournament | None = None):
        super().__init__(parent)

        self.config(background="#BCBABE")

        self.table = TableFrame(self, table_settings={
            'selectable': True,
            'max_one_selection': True,
        })
        self.paused_view = ResizingLabel(self, maxsize=16)

        self._is_table_visible = False

        self.update_tournament_view(tournament, page=-1)

    def update_tournament_view(self, tournament: InteractiveTournament | None, *, page: int):
        self.__place_layout_if_necesary(tournament)

        if tournament is None:
            return

        updaters = [
            self._update_starting_list_view,
            *[lambda t, i2=i: self._update_round_view(t, i2) for i in range(tournament.round_count)],
            *([self._update_results_view] if tournament.is_finished() else []),
        ]

        # noinspection PyArgumentList
        updaters[page](tournament)

    def __place_layout_if_necesary(self, tournament: InteractiveTournament | None):
        if tournament is None:
            self.table.set_data([])
            self.table.place_forget()
            self.paused_view.place_forget()
            self._is_table_visible = False
        elif not self._is_table_visible:
            self.table.place(anchor='n', relx=.5, y=40, relwidth=.8, relheight=.8)
            self.paused_view.place(relx=0, rely=1, y=-100, relwidth=1, height=80)
            self._is_table_visible = True

    def _update_starting_list_view(self, tournament: InteractiveTournament):
        headers = ['#', 'Gracz', 'Ranking']
        starting_list = zip(
            itertools.count(start=1),
            (self.__format_player(p) for p in tournament.players),
            (p.rating for p in tournament.players),
        )

        self.table.set_data([headers, *starting_list])
        self.table.columns_weights = [1, 10, 5]
        self.paused_view.config(text='')

    def _update_round_view(self, tournament: InteractiveTournament, index: int):
        round_ = tournament.get_round(index)

        headers = ['#', 'Biały', 'Wynik', 'Czarny']
        data = list(
            (
                i,
                self.__format_player_with_rating_change(tournament.players[white],
                                                        tournament.stats.recent_rating_changes[white]),
                self.__format_game_result(result),
                self.__format_player_with_rating_change(tournament.players[black],
                                                        tournament.stats.recent_rating_changes[black]),
            )
            for i, ((white, black), result) in enumerate(zip(round_.pairs, round_.results), start=1)
        )

        self.table.set_data([headers, *data])
        self.table.columns_weights = [1, 7, 3, 7]
        self.paused_view.config(text=self.__create_pause_msg(tournament))

    def __create_pause_msg(self, tournament: InteractiveTournament) -> str:
        paused = tournament.get_round().pause
        epsilon = '...' if len(paused) > 4 else ''
        return 'Pauza: ' + ', '.join(self.__format_player_from_id(tournament, pid) for pid in list(paused)[:4]) + epsilon

    def _update_results_view(self, tournament: InteractiveTournament):
        headers = ['#', 'Gracz', 'Punkty']
        scoreboard = tournament.get_id_scoreboard()
        scoreboard = list(
            (
                pos,
                self.__format_player_with_rating_change(tournament.players[player_id],
                                                        tournament.stats.ratings[player_id] - tournament.players[
                                                            player_id].rating),
                self.__format_points(points),
            )
            for pos, player_id, points in scoreboard
        )

        self.table.set_data([headers, *scoreboard])
        self.table.columns_weights = [1, 7, 5]
        self.paused_view.config(text='')

    def __format_player_with_rating_change(self, player: Player, rating_change: float):
        return PlayerWithRatingField(self.table.container, player=player, rating_change=rating_change)

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

    @classmethod
    def __format_points(cls, points: tuple[float, ...]):
        return '\t'.join(map(cls.__parse_int_float, points))

    @staticmethod
    def __parse_int_float(number: int | float) -> str:
        return str(int(number)) if number.is_integer() else str(number)
