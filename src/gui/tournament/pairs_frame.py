import tkinter as tk
from typing import Optional

import src.gui.gui_utils as utils
from src.algorithms.tournament import Tournament
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


class WaitingFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def set_players(self, players: list[Player]):
        print(players)


class PairsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(padx=20, pady=20, bg='#efefef')

        self.table = utils.Table(self, style_prefix='pairs_frame', style_theme='clam')
        self.table.place(relheight=1, relwidth=1)

        self.waiting_frame = WaitingFrame(self)
        self._place_waiting_frame()

        self.table.style_headings(font=('Calibri', 20, 'bold'))
        self.table.style_body(highlightthickness=0, bd=0, font=('Calibri', 14), rowheight=40)
        self.table.style_even(background='#cfcfcf')
        self.table.style_odd(background='white')

        self.first_page_players: list[Player] = []

    def get_selected_players(self) -> list[Player]:
        if self.table['columns'] != FIRST_COLUMNS[0]:
            raise Exception('Cannot get selected player ids when not first page is active')

        selected_players = []
        for row_id in self.table.get_selected_ids():
            player = self.first_page_players[row_id]
            selected_players.append(player)

        return selected_players

    def _update_rows(self, rows: list[tuple], cmp_slice: Optional[slice] = None):
        prev_row = None
        pos = 0
        while rows:
            row = rows.pop(0)

            if cmp_slice is None:
                pos += 1
            elif prev_row is None or prev_row[cmp_slice] != row[cmp_slice]:
                pos += 1

            self.table.add_row(pos, *row)
            prev_row = row

    def _place_waiting_frame(self):
        self.waiting_frame.place(relx=1 - WAITING_SIZE[0], rely=1 - WAITING_SIZE[1], relwidth=WAITING_SIZE[0], relheight=WAITING_SIZE[1])

    def _update_waiting(self, players: Optional[list[Player]]):
        if players is None:
            self.waiting_frame.place_forget()
            return

        self._place_waiting_frame()
        self.waiting_frame.set_players(players)

    def update_first(self, tournament: Tournament):
        self.table.set_columns(*FIRST_COLUMNS)

        self.first_page_players = sorted(tournament.players, key=lambda p: p.rating, reverse=True)

        self._update_rows([(player, player.rating) for player in self.first_page_players])
        self._update_waiting(None)

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
        ], slice(2, 3))
        self._update_waiting(None)
