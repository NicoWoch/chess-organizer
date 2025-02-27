import tkinter as tk
from typing import Optional

from src.algorithms.tournament import Tournament
from src.gui.widgets.colorful_label import ColorfulLabel
from src.gui.widgets.table import ScrollableTableFrame
from src.player import Player

STARTING_TABLE_STYLE = {
    'name': 'starting',
    'columns_count': 3,
    'header': ['#', 'Gracz', 'Ranking'],
    'columns_weights': [50, 350, 250],
    'header_height': 30,
    'row_height': 25,
    'header_bg': '#BDA184',
    'row_bg': '#eee',
    'odd_row_bg': '#fff',
    'selected_bg': '#ADD8E6',
    'header_fg': 'black',
    'row_fg': 'black',
    'font': ('Arial', 13),
    'header_font': ('Roboto', 17),
}

PAIRING_TABLE_STYLE = {
    'name': 'pairing',
    'columns_count': 4,
    'header': ['#', 'Białe', 'Czarne', 'Punkty'],
    'columns_weights': [50, 250, 250, 100],
    'header_height': 30,
    'row_height': 25,
    'header_bg': '#BDA184',
    'row_bg': '#eee',
    'odd_row_bg': '#fff',
    'selected_bg': '#ADD8E6',
    'header_fg': 'black',
    'row_fg': 'black',
    'font': ('Arial', 13),
    'header_font': ('Roboto', 17),
    'max_selection': 1,
}

FINISH_TABLE_STYLE = {
    'name': 'finish',
    'columns_count': 4,
    'header': ['#', 'Gracz', 'Zmiana rankingu', 'Punkty'],
    'columns_weights': [50, 250, 150, 120],
    'header_height': 30,
    'row_height': 25,
    'header_bg': '#BDA184',
    'row_bg': '#eee',
    'odd_row_bg': '#fff',
    'selected_bg': '#ADD8E6',
    'header_fg': 'black',
    'row_fg': 'black',
    'font': ('Arial', 13),
    'header_font': ('Roboto', 17),
    'max_selection': 0,
}


class PauseFrame(tk.Label):
    def __init__(self, parent):
        super().__init__(parent)

        self['background'] = '#efefef'
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

        scrollable_table = ScrollableTableFrame(self)
        self.table = scrollable_table.table
        self.table.configure(bg='#efefef')
        self.table.change_table_style(STARTING_TABLE_STYLE)

        self.pause_frame = PauseFrame(self)

        scrollable_table.place(relheight=.95, relwidth=1)
        self.pause_frame.place(rely=0.95, relwidth=1, relheight=0.05)

        self.first_page_players: list[Player] = []

    def get_selected_players(self) -> list[Player]:
        if self.table.style_name != STARTING_TABLE_STYLE['name']:
            raise Exception('Cannot get selected player ids when not first page is active')

        selected_players = []
        for row_id in self.table.get_selection():
            player = self.first_page_players[row_id]
            selected_players.append(player)

        return selected_players

    def _update_waiting(self, players: Optional[list[Player]]):
        self.pause_frame.set_players(players or [])

    def update_first(self, tournament: Tournament):
        self.table.change_table_style(STARTING_TABLE_STYLE)

        self.first_page_players = sorted(tournament.players, key=lambda p: (p.surname, p.name))

        self.table.update_table([
            (i, player, player.rating)
            for i, player in enumerate(self.first_page_players, start=1)
        ])
        self._update_waiting(None)

    def update_pairing(self, tournament: Tournament, round_id: int):
        self.table.change_table_style(PAIRING_TABLE_STYLE)

        self.table.update_table([
            (i, game.white, game.black, game.result.value)
            for i, game in enumerate(tournament.get_round(round_id), start=1)
        ])
        self._update_waiting(tournament.get_pause(round_id))

    def update_last(self, tournament: Tournament):
        self.table.change_table_style(FINISH_TABLE_STYLE)

        ratings_labels = {
            tournament.players[i]:
                self.__create_ratings_label(tournament.ratings_before[i], tournament.ratings_after[i])
            for i in range(tournament.players_count)
        }

        self.table.update_table([
            (pos, player, ratings_labels[player], str(points))
            for pos, player, points in tournament.get_scoreboard()
        ])
        self._update_waiting(None)

    def __create_ratings_label(self, old_rating: int, new_rating: int):
        deviation = new_rating - old_rating

        if deviation >= 0:
            deviation_str = f'(+{deviation})'.ljust(6)
        else:
            deviation_str = f'(-{abs(deviation)})'.ljust(6)

        text = f'{str(old_rating).rjust(5)} {deviation_str}-> {str(new_rating).rjust(5)}  '

        lbl = ColorfulLabel(self.table, initial_text=text)
        lbl.colorize_regex(r'([\(\)]|->)', '#404040')
        lbl.colorize_regex(r'(^\s+\d+)', '#1f1f1f')

        if new_rating != old_rating:
            lbl.colorize_regex(r'\(([+\-]\d*)\)', 'green' if new_rating > old_rating else 'red')

        return lbl
