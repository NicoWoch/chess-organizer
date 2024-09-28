import tkinter as tk
from abc import ABC, abstractmethod

from src.tournament.round import GameResult


class NavBarListener(ABC):
    @abstractmethod
    def show_tournament_explorer(self): ...

    @abstractmethod
    def show_tournament_creator(self): ...

    @abstractmethod
    def show_players_explorer(self): ...

    @abstractmethod
    def next_round(self): ...

    @abstractmethod
    def remove_last_round(self): ...

    @abstractmethod
    def finish(self): ...

    @abstractmethod
    def set_selected_result(self, result: GameResult | None): ...

    @abstractmethod
    def edit_pairing(self): ...


class Navbar(tk.Frame):
    def __init__(self, parent, *, listener: NavBarListener):
        super().__init__(parent)

        self.config(background="#384B70")

        btn = tk.Button(self, text="SHOW TOURNAMENTS", command=listener.show_tournament_explorer)
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="NEW TOURNAMENT", command=listener.show_tournament_creator)
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="NEXT ROUND", command=listener.next_round)
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="REMOVE LAST ROUND", command=listener.remove_last_round)
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="WHITE WIN", bg='green', command=lambda: listener.set_selected_result(GameResult.WIN))
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="DRAW", bg='green', command=lambda: listener.set_selected_result(GameResult.DRAW))
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="WHITE LOST", bg='green', command=lambda: listener.set_selected_result(GameResult.LOSE))
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="CLEAR RESULT", bg='green', command=lambda: listener.set_selected_result(None))
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="EDIT PAIRING", command=listener.edit_pairing)
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="FINISH", command=listener.finish)
        btn.pack(side=tk.LEFT)
        btn = tk.Button(self, text="SHOW PLAYERS", command=listener.show_players_explorer)
        btn.pack(side=tk.LEFT)
