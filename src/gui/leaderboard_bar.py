import tkinter as tk

from src.gui.widgets.resizing_widgets import ResizingLabel
from src.gui.widgets.table_frame import TableFrame
from src.tournament.interactive_tournament import InteractiveTournament
from src.tournament.player import Player


class LeaderboardBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(background="#e0c4ad")

        label = ResizingLabel(self, text="Leaderboard", relwidth=.7, maxsize=30)
        label.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.table = TableFrame(self, bg='#917762', table_settings={
            'font': ('Comic Sans MS', 10)
        })
        self.table.columns_weights = [1, 10, 5]

        self.table.pack(side=tk.TOP, fill=tk.X, padx=2, pady=10)

    def update_leaderboard(self, tournament: InteractiveTournament | None):
        if tournament is None or not (tournament.is_running() or tournament.is_finished()):
            self.table.set_data([[]])
            return

        scoreboard = tournament.get_player_scoreboard()

        headers = ['#', 'Gracz', 'Punkty']
        rows = [
            [
                pos,
                self.__format_player(player),
                self.__format_points(points),
            ]
            for pos, player, points in scoreboard
        ]

        self.table.set_data([headers, *rows])

    @staticmethod
    def __format_player(player: Player):
        return player.name

    @classmethod
    def __format_points(cls, points: tuple[float, ...]):
        return ' '.join(map(cls.__parse_int_float, points))

    @staticmethod
    def __parse_int_float(number: int | float) -> str:
        return str(int(number)) if number.is_integer() else str(number)
