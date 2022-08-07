import tkinter as tk

import src.gui.gui_utils as utils
from src.algorithms.tournament import Game
from src.player import Player

PAIRING_COLUMNS = [
    ('#', 'Białe', 'Czarne', 'Punkty'),
    (50, 250, 250, 100)
]

LIST_COLUMNS = [
    ('#', 'Gracz', 'Ranking'),
    (50, 350, 250)
]


class PairsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(padx=20, pady=20, bg='#efefef')

        self.table = utils.Table(self, style_prefix='pairs_frame', style_theme='clam')
        self.table.place(relheight=1, relwidth=1)

        self.table.style_headings(font=('Calibri', 20, 'bold'))
        self.table.style_body(highlightthickness=0, bd=0, font=('Calibri', 14), rowheight=40)
        self.table.style_even(background='#cfcfcf')
        self.table.style_odd(background='white')

    def update_pairing(self, pairing: list[Game]):
        self.table.set_columns(*PAIRING_COLUMNS)

        for i, game in enumerate(pairing):
            self.table.add_row(i + 1, game.white, game.black, game.result.value)

    def update_list(self, players: list[Player]):
        self.table.set_columns(*LIST_COLUMNS)

        for i, player in enumerate(players):
            self.table.add_row(i + 1, str(player), player.rating)
