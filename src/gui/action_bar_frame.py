import tkinter as tk
from abc import ABC, abstractmethod

from src.gui import utils
from src.algorithms.constants import Result


class ActionBarListener(ABC):
    @abstractmethod
    def set_result(self, result: Result): ...

    @abstractmethod
    def next_round(self): ...

    @abstractmethod
    def end_tournament(self): ...

    @abstractmethod
    def browse_players(self): ...

    @abstractmethod
    def remove_players(self): ...

    @abstractmethod
    def browse_tournaments(self, create=False): ...


class ActionBarFrame(tk.Frame):
    def __init__(self, parent, listener: ActionBarListener):
        super().__init__(parent)

        self.listener = listener
        self.make_gui()

    def make_gui(self):
        utils.create_image_action_bar(self, [
            utils.Action(
                'throphy.png',
                lambda: self.listener.browse_tournaments(create=True),
                tk.LEFT, tooltip='Stwórz turniej',
            ),
            utils.Action(
                'throphy_ended.png',
                self.listener.browse_tournaments,
                tk.LEFT, tooltip='Przeglądaj turnieje',
            ),
            utils.Action(
                'white_pawn.png',
                lambda: self.listener.set_result(Result.White),
                tk.CENTER, tooltip='Białe wygrały',
            ),
            utils.Action(
                'black_pawn.png',
                lambda: self.listener.set_result(Result.Black),
                tk.CENTER, tooltip='Czarne wygrały',
            ),
            utils.Action(
                'draw.png',
                lambda: self.listener.set_result(Result.Draw),
                tk.CENTER, tooltip='Remis',
            ),
            utils.Action(
                'green_flag.png',
                self.listener.next_round,
                tk.CENTER, tooltip='Następna runda',
            ),
            utils.Action(
                'red_flag.png',
                self.listener.end_tournament,
                tk.CENTER, tooltip='Koniec turnieju'
            ),
            utils.Action(
                'player.png',
                self.listener.browse_players,
                tk.RIGHT, tooltip='Przeglądaj graczy',
            ),
            utils.Action(
                'player_remove.png',
                self.listener.remove_players,
                tk.RIGHT, tooltip='Usuń gracza',
            ),
        ], (50, 50), padx=20, bg='#c9d8e6', active_bg='#a3afe6') \
            .grid(sticky='nesw')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
