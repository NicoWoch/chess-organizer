import tkinter as tk

from src.gui.content_frame import ContentFrame
from src.gui.leaderboard_bar import LeaderboardBar
from src.gui.navbar import Navbar, NavBarListener
from src.gui.rounds_bar import RoundsBar
from src.gui.subwindows.pairing_editor import PairingEditor
from src.tournament.interactive_tournament import InteractiveTournament
from src.tournament.pairing.dutch_pairer import DutchPairer
from src.tournament.player import Player
from src.tournament.round import GameResult, Round
from src.tournament.scoring.buchholz_scorer import BuchholzScorer


class App(tk.Tk, NavBarListener):
    def __init__(self):
        super().__init__()

        self.geometry('1200x800')
        self.title('Chess Organizer V1.0')
        self.minsize(470, 300)
        self.config(background="black")

        self.tournament: InteractiveTournament | None = None

        self.__define_layout()

    def __define_layout(self):
        vertical_pane = tk.Frame(self, background='yellow')
        vertical_pane.pack(fill=tk.BOTH, expand=True)

        horizontal_pane = tk.PanedWindow(vertical_pane, orient=tk.HORIZONTAL, bg='#333333', borderwidth=0, sashwidth=3)

        self.navbar = Navbar(vertical_pane, listener=self)
        self.content_frame = ContentFrame(horizontal_pane)
        self.rounds_bar = RoundsBar(horizontal_pane, self.__update_tournament_view)
        self.leaderboard_bar = LeaderboardBar(horizontal_pane)

        self.navbar.pack(fill=tk.X)
        horizontal_pane.pack(fill=tk.BOTH, expand=True)

        horizontal_pane.add(self.rounds_bar, minsize=100, width=170)
        horizontal_pane.add(self.content_frame, minsize=250, width=780)
        horizontal_pane.add(self.leaderboard_bar, minsize=120, width=300)

    def load_tournament(self, tournament: InteractiveTournament):
        if self.tournament is not None:
            self.unload_tournament()

        self.tournament = tournament
        self._reload_tournament()

    def unload_tournament(self):
        if self.tournament is None:
            return

        self.tournament = None
        self._reload_tournament()

    def _reload_tournament(self):
        print('reload tournament')
        self.rounds_bar.update_tournament_pages(self.tournament)
        self.rounds_bar.select(-1)
        self.leaderboard_bar.update_leaderboard(self.tournament)

    def __update_tournament_view(self, page: int):
        self.content_frame.update_tournament_view(tournament=self.tournament, page=page)
        self.content_frame.table.clear_selection()

    def sample_tournament(self):
        tournament = InteractiveTournament()
        tournament.settings.scorer = BuchholzScorer()

        tournament.add_player(Player('Adam', 'Nowak', 1500))
        tournament.add_player(Player('Celina', 'Kowalska', 1400))
        tournament.add_player(Player('Janusz', 'z Polski', 1200))
        tournament.add_player(Player('Januszka', 'z Polski', 1300))
        tournament.add_player(Player('Janusz2', 'z Podlasia', 1000))
        tournament.next_round(DutchPairer())
        tournament.set_result(0, GameResult.WIN)

        self.load_tournament(tournament)

    def next_round(self):
        self.tournament.next_round(DutchPairer())
        self._reload_tournament()

    def remove_last_round(self):
        self.tournament.remove_last_round()
        self._reload_tournament()

    def finish(self):
        self.tournament.finish()
        self._reload_tournament()

    def set_selected_result(self, result: GameResult | None):
        if self.rounds_bar.is_first_page() or not self.rounds_bar.is_last_page() or self.tournament.is_finished():
            return

        selected = {x - 1 for x in self.content_frame.table.get_selection()}

        for table_id in selected:
            self.tournament.set_result(table_id, result)

        self._reload_tournament()

    def edit_pairing(self):
        if self.tournament is None or not self.tournament.is_running():
            return

        PairingEditor(self, self.tournament, self._apply_last_round)

    def _apply_last_round(self, round_: Round):
        self.tournament.remove_last_round()
        self.tournament.next_round(round_.pairs)

        for i, result in enumerate(round_.results):
            self.tournament.set_result(i, result)

        self._reload_tournament()

