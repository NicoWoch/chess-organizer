import tkinter as tk

from src.algorithms.constants import Points
from src.gui.widgets.table import ScrollableTableFrame
from src.player import Player

SCOREBOARD_TABLE_STYLE = {
    'columns_count': 3,
    'columns_weights': (1, 7, 4),
    'row_height': 22,
    'font': ('Arial', 11),
    'row_bg': '#eee',
    'odd_row_bg': '#fff',
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

        tk.Label(self, text='Tablica Wyników', bg='#ccc', font='Arial 16', justify='center') \
            .place(relwidth=1, height=40)
        scrollable_table.place(y=40, relwidth=1, height=-40, relheight=1)

    def update_scoreboard(self, scoreboard: list[tuple[int, Player, Points]]):
        self.table.update_table([
            (pos, str(player), str(score))
            for pos, player, score in scoreboard
        ])
