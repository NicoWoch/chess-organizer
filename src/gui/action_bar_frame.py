import tkinter as tk
from abc import ABC, abstractmethod

import src.gui.gui_utils as utils
from src.algorithms.tournament import Result


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
    def browse_tournaments(self): ...


class ActionBarFrame(tk.Frame):
    def __init__(self, parent, listener: ActionBarListener):
        super().__init__(parent)

        self.listener = listener

        self.config(bg='#8c5ccc')
        self.make_gui()

    def make_gui(self):
        utils.create_image_action_bar(self, [
            utils.Action('throphy.png', self.listener.browse_tournaments, tk.LEFT),
            utils.Action('white_pawn.png', lambda: self.listener.set_result(Result.White), tk.CENTER),
            utils.Action('black_pawn.png', lambda: self.listener.set_result(Result.Black), tk.CENTER),
            utils.Action('draw_icon.png', lambda: self.listener.set_result(Result.Draw), tk.CENTER),
            utils.Action('green_flag.png', self.listener.next_round, tk.CENTER),
            utils.Action('red_flag.png', self.listener.end_tournament, tk.CENTER),
            utils.Action('player.png', self.listener.browse_players, tk.RIGHT),
            utils.Action('player_minus.png', self.listener.remove_players, tk.RIGHT),
        ], (50, 50), padx=20).grid(sticky='nesw')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
