import tkinter as tk
from typing import Generator

from src.algorithms.constants import Points
from src.gui import utils
from src.gui.widgets.table import Table
from src.player import Player

SCOREBOARD_STYLE = {
    'header': {
        'height': 0,
        'padding': 0,
    },
    'row': {
        'height': 22,
        'font': 'Arial 11',
    },
    'scrollbar': {
        'width': 14,
    }
}


class ScoreboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief='groove', borderwidth=3)

        self.table = Table(self)
        utils.update_styles(self.table.style, SCOREBOARD_STYLE)
        self.table.set_checkmarks_state(False)
        self.table.set_columns(['', '', ''], [1, 3, 2])

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        tk.Label(self, text='Tablica Wyników', bg='#ccc', font='Arial 16', justify='center') \
            .place(relwidth=1, height=40)
        self.table.place(y=40, relwidth=1, height=-40, relheight=1)

    def update_scoreboard(self, scoreboard: list[tuple[int, Player, Points]]):
        self.table.clear_rows()

        for pos, player, score in scoreboard:
            self.table.add_row(pos, str(player), str(score))

        self.table.redraw_rows()
