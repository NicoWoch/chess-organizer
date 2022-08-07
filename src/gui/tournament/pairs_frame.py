import tkinter as tk
from typing import Optional

import src.gui.gui_utils as utils
from src.algorithms.tournament import Game, Tournament

FIRST_COLUMNS = [
    ('#', 'Gracz', 'Ranking'),
    (50, 350, 250)
]

PAIRING_COLUMNS = [
    ('#', 'Białe', 'Czarne', 'Punkty'),
    (50, 250, 250, 100)
]

LAST_COLUMNS = [
    ('#', 'Gracz', 'Zmiana rankingu', 'Punkty'),
    (50, 250, 230, 120)
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

    def _update_rows(self, rows: list[tuple], cmp_slice: Optional[slice] = None):
        prev_row = None
        pos = 0
        while rows:
            row = rows.pop(0)

            if cmp_slice is None:
                pos += 1
            elif prev_row[cmp_slice] != row[cmp_slice]:
                pos += 1

            self.table.add_row(pos, *row)
            prev_row = row


    def update_first(self, tournament: Tournament):
        self.table.set_columns(*FIRST_COLUMNS)

        sorted_players = sorted(tournament.players, key=lambda p: p.rating, reverse=True)

        self._update_rows([(player, player.rating) for player in sorted_players])

    def update_pairing(self, pairing: list[Game]):
        self.table.set_columns(*PAIRING_COLUMNS)

        self._update_rows([(game.white, game.black, game.result.value) for game in pairing])

    def update_last(self, tournament: Tournament):
        self.table.set_columns(*LAST_COLUMNS)

        self._update_rows([
            (
                tournament.players[i],
                f'{tournament.old_ratings[i]} -> {tournament.new_ratings[i]}',
                ',   '.join(map(str, tournament.get_points(i)))
            )
            for i in tournament.get_scoreboard_ids()
        ])
