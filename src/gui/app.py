import tkinter as tk

from src.gui.content_frame import ContentFrame
from src.gui.leaderboard_bar import LeaderboardBar
from src.gui.navbar import Navbar
from src.gui.rounds_bar import RoundsBar
from src.tournament.interactive_tournament import InteractiveTournament
from src.tournament.pairing.dutch_pairer import DutchPairer
from src.tournament.player import Player
from src.tournament.round import GameResult


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('1200x800')
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
        self.rounds_bar = RoundsBar(horizontal_pane, self._update_tournament_view)
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
        self._update_rounds_bar()
        self.rounds_bar.select(-1)

    def unload_tournament(self):
        if self.tournament is None:
            return

        self.tournament = None
        self._update_rounds_bar()
        self.rounds_bar.select(-1)

    def _update_rounds_bar(self):
        self.rounds_bar.update_tournament_pages(self.tournament)

    def _update_tournament_view(self, page: int):
        self.content_frame.update_tournament_view(tournament=self.tournament, page=page)

    def button_1(self):
        tournament = InteractiveTournament()
        tournament.add_player(Player('Adam', 'Nowak', 1500))
        tournament.add_player(Player('Celina', 'Kowalska', 1400))
        tournament.add_player(Player('Janusz', 'z Polski', 1200))
        tournament.next_round(DutchPairer())
        tournament.set_result(0, GameResult.WIN)

        self.load_tournament(tournament)

    def button_2(self):
        self.unload_tournament()

    def button_3(self):
        self.tournament.finish()
        self._update_rounds_bar()
        self.rounds_bar.select(-1)

    def button_4(self):
        self.tournament.next_round(DutchPairer())
        self.tournament.set_result(0, GameResult.DRAW)
        self._update_rounds_bar()
        self.rounds_bar.select(-1)

    def button_5(self):
        pass

