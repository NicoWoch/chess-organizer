import tkinter as tk

from src.algorithms.old_swiss_frames.pairs_frame import PairsFrame
from src.algorithms.old_swiss_frames.rounds_frame import RoundsFrame


class SwissFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.rounds_frame = RoundsFrame(self)
        self.rounds_frame.grid(row=0, column=0, sticky='nesw')

        self.pairs_frame = PairsFrame(self)
        self.pairs_frame.grid(row=0, column=1, sticky='nesw')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.rowconfigure(0, weight=1)
