import tkinter as tk

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
        super().__init__(parent)

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

        self.last_pos = 0
        self.last_score = None

    def _add_player(self, player: Player, score: tuple):
        if self.last_score == score:
            self.table.add_row(self.last_pos, str(player), str(score))
        else:
            self.table.add_row(self.last_pos + 1, str(player), str(score))
            self.last_pos += 1

        self.last_score = score

    def update_scoreboard(self, scoreboard: list[tuple[Player, tuple]]):
        self.last_pos = 0
        self.last_score = None

        self.table.clear_rows()

        for score in scoreboard:
            self._add_player(score[0], score[1])

        self.table.redraw_rows()
