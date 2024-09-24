import tkinter as tk
from abc import ABC, abstractmethod

from src.tournament.round import GameResult


class NavBarListener(ABC):
    @abstractmethod
    def sample_tournament(self): ...

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

        btn1 = tk.Button(self, text="SAMPLE TOURNAMENT", command=listener.sample_tournament)
        btn1.pack(side=tk.LEFT)
        btn2 = tk.Button(self, text="NEXT ROUND", command=listener.next_round)
        btn2.pack(side=tk.LEFT)
        btn3 = tk.Button(self, text="REMOVE LAST ROUND", command=listener.remove_last_round)
        btn3.pack(side=tk.LEFT)
        btn4 = tk.Button(self, text="WHITE WIN", bg='green', command=lambda: listener.set_selected_result(GameResult.WIN))
        btn4.pack(side=tk.LEFT)
        btn5 = tk.Button(self, text="DRAW", bg='green', command=lambda: listener.set_selected_result(GameResult.DRAW))
        btn5.pack(side=tk.LEFT)
        btn6 = tk.Button(self, text="WHITE LOST", bg='green', command=lambda: listener.set_selected_result(GameResult.LOSE))
        btn6.pack(side=tk.LEFT)
        btn7 = tk.Button(self, text="CLEAR RESULT", bg='green', command=lambda: listener.set_selected_result(None))
        btn7.pack(side=tk.LEFT)
        btn8 = tk.Button(self, text="EDIT PAIRING", command=listener.edit_pairing)
        btn8.pack(side=tk.LEFT)
        btn8 = tk.Button(self, text="FINISH", command=listener.finish)
        btn8.pack(side=tk.LEFT)
