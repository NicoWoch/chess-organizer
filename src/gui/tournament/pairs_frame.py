import tkinter as tk
from typing import Optional

import src.gui.gui_utils as utils
from src.algorithms.tournament import Game, Tournament
from src.player import Player

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

WAITING_COLUMNS = [
    ('PAUZA',),
    (1,)
]
WAITING_SIZE = 0.3, 0.2


class PairsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(padx=20, pady=20, bg='#efefef')

        self.table = utils.Table(self, style_prefix='pairs_frame', style_theme='clam')
        self.table.place(relheight=1, relwidth=1)

        self.waiting_table = utils.Table(self, style_prefix='pairs_frame')
        self.waiting_table.place(relx=1 - WAITING_SIZE[0], rely=1 - WAITING_SIZE[1], relwidth=WAITING_SIZE[0], relheight=WAITING_SIZE[1])
        self.waiting_table.set_columns(*WAITING_COLUMNS)

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

    def _update_waiting(self, players: list[Player]):
        self.waiting_table.clear_rows()

        for player in players:
            self.waiting_table.add_row(player)

    def update_first(self, tournament: Tournament):
        self.table.set_columns(*FIRST_COLUMNS)

        sorted_players = sorted(tournament.players, key=lambda p: p.rating, reverse=True)

        self._update_rows([(player, player.rating) for player in sorted_players])
        self._update_waiting([])

    def update_pairing(self, tournament: Tournament, round_id: int):
        self.table.set_columns(*PAIRING_COLUMNS)

        self._update_rows([(game.white, game.black, game.result.value) for game in tournament.get_round(round_id)])
        self._update_waiting(tournament.get_waiting_players(round_id))

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
        self._update_waiting([])
