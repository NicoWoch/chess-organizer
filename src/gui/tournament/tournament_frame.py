import tkinter as tk

from src.gui.tournament.pairs_frame import PairsFrame
from src.gui.tournament.rounds_frame import RoundsFrame
from src.gui.tournament.scoreboard_frame import ScoreboardFrame


class TournamentFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.rounds_frame = RoundsFrame(self)
        self.rounds_frame.grid(row=0, column=0, sticky='nesw')

        self.pairs_frame = PairsFrame(self)
        self.pairs_frame.grid(row=0, column=1, sticky='nesw')

        self.scoreboard_frame = ScoreboardFrame(self)
        self.scoreboard_frame.grid(row=0, column=2, sticky='nesw')

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=1)
