import tkinter as tk

from src.algorithms.constants import Points
from src.gui.widgets.points_view import PointsView, POINTS_VIEW_STYLE
from src.gui.widgets.table import ScrollableTableFrame
from src.player import Player

SCOREBOARD_TABLE_STYLE = {
    'columns_count': 3,
    'columns_weights': (1, 7, 5),
    'row_height': 27,
    'font': ('Arial', 12),
    'row_bg': '#eee',
    'odd_row_bg': '#fff',
    'max_selection': 0,
}


class ScoreboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief='groove', borderwidth=1, background='black')

        scrollable_table = ScrollableTableFrame(self, scrollbar_width=10)

        self.table = scrollable_table.table
        self.table.change_table_style(SCOREBOARD_TABLE_STYLE)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.configure(bg='#BDA184')

        tk.Label(self, text='Tablica Wyników', bg=self['bg'], font='Roboto 16', justify='center') \
            .place(relwidth=1, height=40)
        scrollable_table.place(y=40, relwidth=1, height=-40 - 5, relheight=1)

    def update_scoreboard(self, scoreboard: list[tuple[int, Player, Points]]):
        self.table.update_table([
            (pos, str(player), PointsView(self.table, score, POINTS_VIEW_STYLE['scoreboard']))
            for pos, player, score in scoreboard
        ])
