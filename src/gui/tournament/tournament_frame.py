import logging
import tkinter as tk
from typing import Optional

from src.algorithms.swiss_tournament import SwissTournament
from src.algorithms.tournament import Tournament
from src.config import Config
from src.db import MainDB
from src.gui.action_bar_frame import ActionBarListener
from src.gui.subwindows.error_window import WindowException, ErrorWindow
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

    def _forget_all(self):
        for slave in self.grid_slaves():
            slave.grid_forget()

        for slave in self.place_slaves():
            slave.place_forget()

    def _ungrid_scoreboard(self):
        self.scoreboard_frame.grid_forget()

    def _update_frame(self, auto_save=True):
        if self.tournament is None:
            self._forget_all()
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
            self.__show_swiss_info_labels()

        if auto_save:
            self.auto_save_tournament()

    def __show_swiss_info_labels(self):
        players_count = len(self.tournament.players)

        for label in self._info_labels:
            label.destroy()

        if players_count >= 2:
            optimum = math.ceil(math.log(players_count, 2))
            # maksimum = (math.factorial(players_count) // (2 * math.factorial(players_count - 2))) / (players_count // 2)

            optimum_label = tk.Label(self, text=f'Optymalna ilość rund: {optimum}', bg='#bfbfbf', font=('Calibri', 9))
            optimum_label.place(x=3, rely=1, y=-25, anchor=tk.W)

            # maximum_label = tk.Label(self, text=f'Maksymalna ilość rund: {maksimum}', bg='#bfbfbf', font=('Calibri', 9))
            # maximum_label.place(x=3, rely=1, y=-25, anchor=tk.W)

            self._info_labels.extend([optimum_label])  # , maximum_label])

    def set_result(self, result):
        assert self.tournament is not None, WindowException(Config.ErrorMsg.TOURNAMENT_NOT_OPENED)
        assert self.tournament.is_started(), WindowException(Config.ErrorMsg.TOURNAMENT_NOT_STARTED)
        assert not self.tournament.is_ended(), WindowException(Config.ErrorMsg.TOURNAMENT_HAS_ENDED)

        if not self.rounds_frame.is_round():
            return

        assert self.rounds_frame.get_active_round() == self.tournament.active_round_id, WindowException(Config.ErrorMsg.CANNOT_EDIT_IN_CLOSED_ROUND)

        selection = self.pairs_frame.table.get_selected_ids()

        assert len(selection) > 0, WindowException(Config.ErrorMsg.TABLE_NOT_SELECTED)

        for i in selection:
            self.tournament.set_result(i, result)

        self.pairs_frame.table.remove_selection()
        self._update_frame()

    def next_round(self):
        assert self.tournament is not None, WindowException(Config.ErrorMsg.TOURNAMENT_NOT_OPENED)
        assert len(self.tournament.players) >= 2, WindowException(Config.ErrorMsg.TOO_LESS_PLAYERS_IN_TOURNAMENT)
        assert not self.tournament.is_ended(), WindowException(Config.ErrorMsg.TOURNAMENT_HAS_ENDED)
        assert self.tournament.has_round_ended(), WindowException(Config.ErrorMsg.NOT_ALL_GAMES_ENDED)

        try:
            self.tournament.next_round()
        except Exception:
            raise AssertionError(WindowException(Config.ErrorMsg.CANNOT_PAIR))

        self.rounds_frame.update_tournament(self.tournament)
        self._update_frame()

    def end_tournament(self):
        assert self.tournament is not None, WindowException(Config.ErrorMsg.TOURNAMENT_NOT_OPENED)
        assert self.tournament.is_started(), WindowException(Config.ErrorMsg.TOURNAMENT_NOT_STARTED)
        assert not self.tournament.is_ended(), WindowException(Config.ErrorMsg.TOURNAMENT_HAS_ENDED)
        assert self.tournament.has_round_ended(), WindowException(Config.ErrorMsg.NOT_ALL_GAMES_ENDED)

        self.tournament.end_tournament()
        self._update_ratings()
        self.rounds_frame.update_tournament(self.tournament)
        self._update_frame()

    def _update_ratings(self):
        db_players = MainDB.load_players()

        not_found_players = []
        for i, (player, new_rating) in enumerate(zip(self.tournament.players, self.tournament.new_ratings)):
            if player not in db_players:
                not_found_players.append(player)
                continue

            db_id = db_players.index(player)
            db_players[db_id].rating = new_rating

        MainDB.save_players(db_players)

        if not_found_players:
            self.after(100, lambda: self.__show_players_not_found_error(not_found_players))

    def __show_players_not_found_error(self, players):
        ErrorWindow(self.winfo_toplevel(), WindowException(
            Config.ErrorMsg.PLAYER_NOT_FOUND.format(players='\n'.join(map(str, players)))
        )).mainloop()

    def browse_players(self):
        players_browser = PlayerBrowserWindow(self, self.add_players)
        players_browser.focus()

    def add_players(self, players):
        assert self.tournament is not None, WindowException(Config.ErrorMsg.TOURNAMENT_NOT_OPENED)
        assert not self.tournament.is_started(), WindowException(Config.ErrorMsg.CANNOT_ADD_PLAYER_WHEN_STARTED)

        for player in players:
            self.tournament.add_player(player)

        self._update_frame()

    def remove_players(self):
        assert self.tournament is not None, WindowException(Config.ErrorMsg.TOURNAMENT_NOT_OPENED)
        assert not self.tournament.is_started(), WindowException(Config.ErrorMsg.CANNOT_REMOVE_PLAYER_WHEN_STARTED)

        selected_players = self.pairs_frame.get_selected_players()

        assert len(selected_players) > 0, WindowException(Config.ErrorMsg.PLAYER_NOT_SELECTED)

        for p in selected_players:
            self.tournament.remove_player(p)

        self.pairs_frame.table.remove_selection()
        self._update_frame()

    def browse_tournaments(self):
        tournament_browser = TournamentBrowserWindow(self, self.open_tournament, self.close_tournament)
        tournament_browser.focus()

    def open_tournament(self, tournament):
        logging.info(f'Changing opened tournament to ({tournament.name=})')
        self.tournament = tournament

        update_title(self.winfo_toplevel(), self.tournament)
        self.rounds_frame.update_tournament(self.tournament)
        self._update_frame()

    def close_tournament(self):
        logging.info(f'Closing tournament')
        self.tournament = None

        update_title(self.winfo_toplevel(), self.tournament)
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
