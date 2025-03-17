import logging
import tkinter as tk
from typing import Optional, Literal

from src.algorithms.swiss_tournament import SwissTournament, get_optimal_swiss_rounds
from src.algorithms.tournament import Tournament
from src.config import Config
from src.db import MainDB
from src.gui.action_bar_frame import ActionBarListener
from src.gui.subwindows.info.confirm_window import ConfirmWindow
from src.gui.subwindows.info.error_window import WindowException, ErrorWindow
from src.gui.subwindows.player_browser_window import PlayerBrowserWindow
from src.gui.subwindows.tournament_browser_window import TournamentBrowserWindow
from src.gui.tournament.pairs_frame import PairsFrame
from src.gui.tournament.rounds_frame import RoundsFrame
from src.gui.tournament.scoreboard_frame import ScoreboardFrame
from src.pdf import pdf
from src.player import Player


def update_title(main_window: tk.Tk, tournament):
    if tournament is None:
        main_window.title(Config.WINDOW_NAME)
    else:
        sep = ' ' * 3 + '-' + ' ' * 3
        main_window.title(Config.WINDOW_NAME + sep + tournament.name)


class TournamentFrame(tk.Frame, ActionBarListener):
    def __init__(self, parent, register_subwindow):
        super().__init__(parent)
        self.tournament: Optional[Tournament] = None
        self.register_subwindow = register_subwindow

        self.rounds_frame = RoundsFrame(self, lambda: self._update_frame(auto_save=False))
        self.pairs_frame = PairsFrame(self)
        self.scoreboard_frame = ScoreboardFrame(self)

        self.columnconfigure(0, weight=1, minsize=40)
        self.columnconfigure(1, weight=7, minsize=50)
        self.rowconfigure(0, weight=1)

        self.rounds_frame.grid(row=0, column=0, sticky='nesw')
        self.pairs_frame.grid(row=0, column=1, sticky='nesw')
        self.scoreboard_frame.grid(row=0, column=2, sticky='nesw')

        self._update_frame()

        self._info_labels: list[tk.Label] = []
        self.bind('<Configure>', lambda _: self.__show_swiss_info_labels())

    def _grid_frame(self, grid_scoreboard: bool):
        self.rounds_frame.grid()
        self.pairs_frame.grid()
        self.update()
        self.rounds_frame.grid()
        self.pairs_frame.grid()

        if grid_scoreboard:
            self.grid_columnconfigure(1, weight=5)
            self.grid_columnconfigure(2, weight=2, minsize=5)
            self.scoreboard_frame.grid()
        else:
            self.grid_columnconfigure(1, weight=7)
            self.grid_columnconfigure(2, weight=0, minsize=5)
            self.scoreboard_frame.grid_remove()

    def _forget_all(self):
        for slave in self.grid_slaves():
            slave.grid_remove()

        for slave in self.place_slaves():
            slave.place_forget()

    def _update_frame(self, auto_save=True):
        if self.tournament is None:
            self._forget_all()
            return

        self.scoreboard_frame.update_scoreboard(self.tournament.create_scoreboard())
        self._grid_frame(grid_scoreboard=self.rounds_frame.is_round())

        if self.rounds_frame.is_registration():
            self.pairs_frame.update_first(self.tournament)
        elif self.rounds_frame.is_results():
            self.pairs_frame.update_last(self.tournament)
        else:
            self.pairs_frame.update_pairing(self.tournament, self.rounds_frame.get_active_round())

        if isinstance(self.tournament, SwissTournament):
            self.__show_swiss_info_labels()

        if auto_save:
            self.auto_save_tournament()

    def __show_swiss_info_labels(self):
        if not isinstance(self.tournament, SwissTournament):
            return

        def after_func():
            players_count = len(self.tournament.players)

            while self._info_labels:
                self._info_labels.pop().place_forget()

            if players_count >= 2:
                optimum = get_optimal_swiss_rounds(self.tournament.players_count)

                optimum_label = tk.Label(self, text=f'Optymalna ilość\nrund:  {optimum}',
                                         font=('Calibri', 9), justify='center')
                optimum_label.place(x=30, rely=1, y=-60, width=self.rounds_frame.winfo_width() - 60, height=40)

                self._info_labels.append(optimum_label)

        self.after(100, after_func)

    def __assert_tournament_opened(self):
        if self.tournament is None:
            raise WindowException(Config.Messages.TOURNAMENT_NOT_OPENED)

    def __assert_tournament_running(self):
        self.__assert_tournament_opened()

        if not self.tournament.is_started:
            raise WindowException(Config.Messages.TOURNAMENT_NOT_STARTED)
        elif self.tournament.is_ended:
            raise WindowException(Config.Messages.TOURNAMENT_HAS_ENDED)

    def __assert_tournament_not_started(self):
        self.__assert_tournament_opened()

        if self.tournament.is_started:
            raise WindowException(Config.Messages.TOURNAMENT_STARTED)

    def __assert_has_round_ended(self):
        self.__assert_tournament_opened()

        if self.tournament.is_ended:
            raise WindowException(Config.Messages.TOURNAMENT_HAS_ENDED)

        if self.tournament.is_started and not self.tournament.are_all_games_finished():
            raise WindowException(Config.Messages.ROUND_NOT_ENDED)

    def __assert_can_make_next_round(self):
        self.__assert_has_round_ended()

        if self.tournament.players_count < 2:
            raise WindowException(Config.Messages.TOO_LESS_PLAYERS_IN_TOURNAMENT)

    def set_result(self, result):
        self.__assert_tournament_running()

        if not self.rounds_frame.is_round():
            return

        if self.rounds_frame.get_active_round() != self.tournament.round_count - 1:
            raise WindowException(Config.Messages.CANNOT_EDIT_IN_CLOSED_ROUND)

        selection = self.pairs_frame.table.get_selection()

        for i in selection:
            self.tournament.set_result(i, result)

        self.pairs_frame.table.remove_selection()
        self._update_frame()

    def next_round(self):
        self.__assert_can_make_next_round()

        try:
            self.tournament.next_round()
        except Exception:
            raise AssertionError(WindowException(Config.Messages.CANNOT_PAIR))

        self.rounds_frame.update_tournament(self.tournament)
        self._update_frame()

    def end_tournament(self):
        self.__assert_tournament_running()
        self.__assert_has_round_ended()

        def confirmed():
            self.tournament.end_tournament()
            self._update_ratings()
            self.rounds_frame.update_tournament(self.tournament)
            self._update_frame()

        ConfirmWindow(self.winfo_toplevel(), Config.Messages.END_THE_TOURNAMENT, confirmed)

    def _update_ratings(self):
        db_players = MainDB.load_players()

        not_found_players = []
        for i, (player, new_rating) in enumerate(zip(self.tournament.players, self.tournament.ratings_after)):
            if player not in db_players:
                not_found_players.append(player)
                continue

            db_id = db_players.index(player)
            db_players[db_id].rating = new_rating

        MainDB.save_players(db_players)

        if not_found_players:
            self.after(100, lambda: self.__show_players_not_found_error(not_found_players))

    def __show_players_not_found_error(self, players: list[Player]):
        ErrorWindow(self.winfo_toplevel(), WindowException(
            Config.Messages.PLAYER_NOT_FOUND.format(players='\n'.join(map(str, players)))
        ))

    def browse_players(self):
        players_browser = PlayerBrowserWindow(self, self.add_players)
        players_browser.focus()
        self.register_subwindow(players_browser)

    def add_players(self, players):
        self.__assert_tournament_not_started()

        already_added_players = []
        for player in players:
            if player in self.tournament.players:
                already_added_players.append(player)
                continue

            self.tournament.add_player(player)

        if already_added_players:
            ErrorWindow(self.winfo_toplevel(), WindowException(
                Config.Messages.PLAYER_ALREADY_ADDED.format(players='\n'.join(map(str, already_added_players)))
            ))

        self._update_frame()

    def remove_players(self):
        self.__assert_tournament_not_started()

        selected_players = self.pairs_frame.get_selected_players()

        for p in selected_players:
            self.tournament.remove_player(p)

        self.pairs_frame.table.remove_selection()
        self._update_frame()

    def browse_tournaments(self, create=False):
        tournament_browser = TournamentBrowserWindow(self, self.open_tournament, self.close_tournament,
                                                     auto_create=create)
        tournament_browser.focus()
        self.register_subwindow(tournament_browser)

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

    def make_pdf_starting_list(self, action: Literal['print', 'save']):
        self.__assert_tournament_opened()

        fpdf = pdf.make_starting_list_pdf(self.tournament.name, self.tournament.players)
        self.__run_pdf_action(fpdf, action)

    def make_pdf_active_pairings(self, action: Literal['print', 'save']):
        self.__assert_tournament_opened()
        if not self.rounds_frame.is_round():
            raise WindowException(Config.Messages.NOT_ON_PAGE_WITH_PAIRS)

        round_id = self.rounds_frame.get_active_round()
        pairings = self.tournament.get_round(round_id)
        pause_players = self.tournament.calculate_pause(round_id)

        fpdf = pdf.make_pairings_pdf(self.tournament.name, round_id, pairings, pause_players)
        self.__run_pdf_action(fpdf, action)

    def make_pdf_results(self, action: Literal['print', 'save']):
        self.__assert_tournament_opened()

        fpdf = pdf.make_results_pdf(self.tournament.name, self.tournament.create_scoreboard())
        self.__run_pdf_action(fpdf, action)

    @classmethod
    def __run_pdf_action(cls, fpdf, action):
        if action == 'print':
            pdf.show_pdf_in_browser(fpdf)
        elif action == 'save':
            pdf.save_pdf_with_dialog(fpdf)
