import tkinter as tk

from src.database import Database
from src.gui.content_frame import ContentFrame
from src.gui.leaderboard_bar import LeaderboardBar
from src.gui.navbar import Navbar, NavBarListener
from src.gui.rounds_bar import RoundsBar
from src.gui.subwindows.pairing_editor import PairingEditor
from src.gui.subwindows.player_explorer import PlayerExplorer
from src.gui.subwindows.tournament_creator import TournamentCreator
from src.gui.subwindows.tournament_explorer import TournamentExplorer
from src.tournament.interactive_tournament import InteractiveTournament
from src.tournament.pairing.dutch_pairer import DutchPairer
from src.tournament.player import Player
from src.tournament.round import GameResult, Round


class App(tk.Tk, NavBarListener):
    def __init__(self, database: Database):
        super().__init__()

        self.database = database

        self.tournament_id: int | None = None
        self.tournament: InteractiveTournament | None = None
        self.opened_windows = set()

        self.__define_layout()

    def __define_layout(self):
        self.geometry('1200x800')
        self.title('Chess Organizer V1.0')
        self.minsize(470, 300)
        self.config(background="black")

        vertical_pane = tk.Frame(self, background='yellow')
        vertical_pane.pack(fill=tk.BOTH, expand=True)

        horizontal_pane = tk.PanedWindow(vertical_pane, orient=tk.HORIZONTAL, bg='#333333', borderwidth=0, sashwidth=3)

        self.navbar = Navbar(vertical_pane, listener=self)
        self.content_frame = ContentFrame(horizontal_pane)
        self.rounds_bar = RoundsBar(horizontal_pane, self.__update_content_view)
        self.leaderboard_bar = LeaderboardBar(horizontal_pane)

        self.navbar.pack(fill=tk.X)
        horizontal_pane.pack(fill=tk.BOTH, expand=True)

        horizontal_pane.add(self.rounds_bar, minsize=100, width=170)
        horizontal_pane.add(self.content_frame, minsize=250, width=780)
        horizontal_pane.add(self.leaderboard_bar, minsize=120, width=300)

    def __auto_save_and_refresh_view(self, *, autosave=True):
        print(f'auto save and refresh of tournament (autosave={autosave})')
        self.rounds_bar.update_tournament_pages(self.tournament)
        self.rounds_bar.select(-1)
        self.leaderboard_bar.update_leaderboard(self.tournament)

        if self.tournament is not None and autosave:
            db = self.database.read()
            db['tournaments'][self.tournament_id] = self.tournament
            self.database.write(db)

    def __update_content_view(self, page: int):
        self.content_frame.update_tournament_view(tournament=self.tournament, page=page)
        self.content_frame.table.clear_selection()

    def load_tournament(self, tournament_id: int):
        if self.tournament is not None:
            self.unload_tournament()

        db = self.database.read()

        self.tournament_id = tournament_id
        self.tournament = db['tournaments'][tournament_id]
        self.__auto_save_and_refresh_view(autosave=False)

    def unload_tournament(self):
        if self.tournament is None:
            return

        self.tournament_id = None
        self.tournament = None
        self.__auto_save_and_refresh_view()

    def create_new_tournament(self, tournament: InteractiveTournament):
        db = self.database.read()
        db['tournaments'].append(tournament)
        self.database.write(db)
        self.load_tournament(len(db['tournaments']) - 1)

    def add_player_to_tournament(self, player: Player):
        self.tournament.add_player(player)
        self.__auto_save_and_refresh_view()

    def remove_player_from_tournament(self, player: Player):
        self.tournament.remove_player(player)
        self.__auto_save_and_refresh_view()

    def show_tournament_explorer(self):
        self.__show_window_once(TournamentExplorer, self.database, open_tournament=self.load_tournament)

    def show_tournament_creator(self):
        self.__show_window_once(TournamentCreator, self.create_new_tournament)

    def show_players_explorer(self):
        self.__show_window_once(PlayerExplorer, self.database, self.add_player_to_tournament)

    def __show_window_once(self, window_class: type[tk.Toplevel], *args, **kwargs):
        if window_class in self.opened_windows:
            return

        window = window_class(self, *args, **kwargs)

        self.opened_windows.add(window_class)
        window.protocol('WM_DELETE_WINDOW', lambda: (self.opened_windows.remove(window_class), window.destroy()))

    def next_round(self):
        self.tournament.next_round(DutchPairer())  # TODO: use other pairers too
        self.__auto_save_and_refresh_view()

    def remove_last_round(self):
        self.tournament.remove_last_round()
        self.__auto_save_and_refresh_view()

    def finish(self):
        self.tournament.finish()
        self.__auto_save_and_refresh_view()

    def set_selected_result(self, result: GameResult | None):
        if not self.rounds_bar.is_last_page():
            return

        results = {(x - 1, result) for x in self.content_frame.table.get_selection()}
        self.tournament.set_results_from_iterable(results)

        self.__auto_save_and_refresh_view()

    def edit_pairing(self):
        if not self.tournament.is_running():
            return

        PairingEditor(self, self.tournament, self._change_round_pairings)

    def _change_round_pairings(self, round_: Round):
        self.tournament.remove_last_round()
        self.tournament.next_round(round_.pairs)

        for i, result in enumerate(round_.results):
            self.tournament.set_result(i, result)

        self.__auto_save_and_refresh_view()
