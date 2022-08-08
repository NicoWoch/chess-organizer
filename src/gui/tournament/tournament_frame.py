import logging
import tkinter as tk
from typing import Optional

from src.algorithms.swiss_tournament import SwissTournament
from src.algorithms.tournament import Tournament
from src.config import Config
from src.db import MainDB
from src.gui.action_bar_frame import ActionBarListener
from src.gui.subwindows.error_window import WindowException
from src.gui.subwindows.player_browser_window import PlayerBrowserWindow
from src.gui.subwindows.tournament_browser_window import TournamentBrowserWindow
from src.gui.tournament.pairs_frame import PairsFrame
from src.gui.tournament.rounds_frame import RoundsFrame
from src.gui.tournament.scoreboard_frame import ScoreboardFrame
import math


def update_title(main_window: tk.Tk, tournament):
    if tournament is None:
        main_window.title(Config.WINDOW_NAME)
    else:
        sep = ' ' * 3 + '-' + ' ' * 3
        main_window.title(Config.WINDOW_NAME + sep + tournament.name)


class TournamentFrame(tk.Frame, ActionBarListener):
    def __init__(self, parent):
        super().__init__(parent)
        self.tournament: Optional[Tournament] = None

        self.rounds_frame = RoundsFrame(self, lambda: self._update_frame(auto_save=False))
        self.pairs_frame = PairsFrame(self)
        self.scoreboard_frame = ScoreboardFrame(self)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=20)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        self._update_frame()

        self._info_labels: list[tk.Label] = []

    def _grid_frame(self, grid_scoreboard=True):
        self.rounds_frame.grid(row=0, column=0, sticky='nesw')
        self.pairs_frame.grid(row=0, column=1, sticky='nesw')

        if grid_scoreboard:
            self.scoreboard_frame.grid(row=0, column=2, sticky='nesw')

    def _ungrid_frame(self):
        self.rounds_frame.grid_forget()
        self.pairs_frame.grid_forget()
        self.scoreboard_frame.grid_forget()

    def _ungrid_scoreboard(self):
        self.scoreboard_frame.grid_forget()

    def _update_frame(self, auto_save=True):
        if self.tournament is None:
            self._ungrid_frame()
            return

        self._grid_frame(grid_scoreboard=self.rounds_frame.is_round())

        if not self.rounds_frame.is_round():
            self._ungrid_scoreboard()

        if self.rounds_frame.is_first():
            self.pairs_frame.update_first(self.tournament)
        elif self.rounds_frame.is_last():
            self.pairs_frame.update_last(self.tournament)
        else:
            self.pairs_frame.update_pairing(self.tournament, self.rounds_frame.get_active_round())

        self.scoreboard_frame.update_scoreboard(self.tournament.get_scoreboard())

        if isinstance(self.tournament, SwissTournament):
            self.__show_optimal_and_max_round_for_swiss()

        if auto_save:
            self.auto_save_tournament()

    def __show_optimal_and_max_round_for_swiss(self):
        players_count = len(self.tournament.players)

        for label in self._info_labels:
            label.destroy()

        if players_count > 2:
            optimum = math.ceil(math.log(players_count, 2))
            maksimum = (math.factorial(players_count) // (2 * math.factorial(players_count - 2))) // (players_count // 2)

            optimum_label = tk.Label(self, text=f'Optymalna ilość rund: {optimum}', bg='#bfbfbf', font=('Calibri', 9))
            optimum_label.place(x=3, rely=1, y=-50, anchor=tk.W)

            maximum_label = tk.Label(self, text=f'Maksymalna ilość rund: {maksimum}', bg='#bfbfbf', font=('Calibri', 9))
            maximum_label.place(x=3, rely=1, y=-25, anchor=tk.W)

            self._info_labels.extend([optimum_label, maximum_label])

    @property
    def active_round(self):
        if self.rounds_frame.is_round():
            return self.tournament.get_round(self.rounds_frame.get_active_round())

    def set_result(self, result):
        if self.tournament is None:
            logging.warning('There is no tournament opened')
            return

        if self.active_round != self.tournament.active_round:
            logging.warning('Tried to change game status in round that ended')
            return

        selection = self.pairs_frame.table.get_selected_ids()

        for i in selection:
            self.tournament.set_result(i, result)

        self.pairs_frame.table.remove_selection()
        self._update_frame()

    def next_round(self):
        if self.tournament is None:
            logging.warning('There is no tournament opened')
            return

        self.tournament.next_round()

        self.rounds_frame.update_tournament(self.tournament)
        self._update_frame()

    def end_tournament(self):
        if self.tournament is None:
            logging.warning('There is no tournament opened')
            return

        self.tournament.end_tournament(MainDB)
        self.rounds_frame.update_tournament(self.tournament)
        self._update_frame()

    def browse_players(self):
        players_browser = PlayerBrowserWindow(self, self.add_players)
        players_browser.focus()

    def add_players(self, players):
        if self.tournament is None:
            logging.warning('There is no tournament opened')
            return

        if self.tournament.is_started():
            raise Exception('Cannot add player to started tournament')

        for player in players:
            self.tournament.add_player(player)

        self._update_frame()

    def remove_players(self):
        if not self.rounds_frame.is_first():
            logging.warning('Tried to remove players when not first page is active')
            return

        selected_players = self.pairs_frame.get_selected_players()

        for p in selected_players:
            self.tournament.remove_player(p)

        self.pairs_frame.table.remove_selection()
        self._update_frame()

    def browse_tournaments(self):
        tournament_browser = TournamentBrowserWindow(self, self.open_tournament)
        tournament_browser.focus()

    def open_tournament(self, tournament):
        logging.info(f'Changing opened tournament to ({tournament.name=})')
        self.tournament = tournament

        update_title(self.winfo_toplevel(), self.tournament)

        self.rounds_frame.update_tournament(self.tournament)
        self._update_frame()

    def auto_save_tournament(self):
        if self.tournament is None:
            return

        logging.info(f'Auto saving opened tournament')

        tournaments = MainDB.load_tournaments()

        for i, t in enumerate(tournaments):
            if t.name == self.tournament.name:
                tournaments[i] = self.tournament
                break
        else:
            raise Exception('Tournament not found when autosaving')

        MainDB.save_tournaments(tournaments)
