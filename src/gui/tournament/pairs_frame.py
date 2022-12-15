import tkinter as tk
from typing import Optional

from src.algorithms.tournament import Tournament
from src.gui.widgets.table import Table, colourfull_label
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


class WaitingFrame(tk.Label):
    def __init__(self, parent):
        super().__init__(parent)

        self['background'] = '#eee'
        self['font'] = ('Calibri', 18)
        self['anchor'] = 'se'

    def set_players(self, players: list[Player]):
        if len(players) == 0:
            self['text'] = ''
        elif len(players) == 1:
            self['text'] = f'Pauza:   {players[0]}'
        else:
            self['text'] = f'Pauza:   {players[0]} + {len(players) - 1} graczy'


class PairsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(padx=20, pady=20, bg='#efefef')

        self.table = Table(self)
        self.table.set_checkmarks_state(False)
        self.table.style['header']['font'] = 'Arial 18'
        self.table.style['row']['font'] = 'Arial 13'
        self.table.style['one_select'] = True
        self.table.place(relheight=.95, relwidth=1)

        self.waiting_frame = WaitingFrame(self)
        self._place_waiting_frame()

        self.first_page_players: list[Player] = []

    def get_selected_players(self) -> list[Player]:
        if self.table.get_columns() != FIRST_COLUMNS[0]:
            raise Exception('Cannot get selected player ids when not first page is active')

        selected_players = []
        for row_id in self.table.get_selection():
            player = self.first_page_players[row_id]
            selected_players.append(player)

        return selected_players

    def _update_rows(self, rows: list[tuple], add_indexes=True):
        for i, row in enumerate(rows, start=1):
            if add_indexes:
                self.table.add_row(i, *row)
            else:
                self.table.add_row(*row)

        self.table.redraw_rows()

    def _place_waiting_frame(self):
        self.waiting_frame.place(rely=0.95, relwidth=1, relheight=0.05)

    def _update_waiting(self, players: Optional[list[Player]]):
        if players is None:
            self.waiting_frame.place_forget()
            return

        self._place_waiting_frame()
        self.waiting_frame.set_players(players)

    def update_first(self, tournament: Tournament):
        self.table.set_columns(*FIRST_COLUMNS)

        self.first_page_players = sorted(tournament.players, key=lambda p: (p.surname, p.name))

        self._update_rows([(player, player.rating) for player in self.first_page_players])
        self._update_waiting(None)

    def update_pairing(self, tournament: Tournament, round_id: int):
        self.table.set_columns(*PAIRING_COLUMNS)

        self._update_rows([(game.white, game.black, game.result.value) for game in tournament.get_round(round_id)])
        self._update_waiting(tournament.get_pause(round_id))

    def update_last(self, tournament: Tournament):
        self.table.set_columns(*LAST_COLUMNS)

        rating_deviations = [new - old for old, new in zip(tournament.ratings_before, tournament.ratings_after)]
        rating_deviations_str = [f'+{dv}' if dv > 0 else f'{dv}' for dv in rating_deviations]
        ratings_labels = {
            tournament.players[i]:
                self.__create_ratings_label(tournament.ratings_before[i], tournament.ratings_after[i], rating_deviations_str[i])
            for i in range(tournament.players_count)
        }

        self._update_rows([(pos, player, ratings_labels[player], str(points))
                           for pos, player, points in tournament.get_scoreboard()], add_indexes=False)
        self._update_waiting(None)

    def __create_ratings_label(self, old_rating: int, new_rating: int, deviation_str: str):
        return colourfull_label(f'{old_rating}  ({deviation_str})    ->     {new_rating}', (
            (len(f'{old_rating}  ('),
             len(f'{old_rating}  ({deviation_str}'),
             ('green' if new_rating > old_rating else ('red' if new_rating < old_rating else 'black'))),
        ))
