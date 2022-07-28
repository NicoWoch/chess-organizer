import tkinter as tk

from src.algorithms.swiss.swiss_frame import SwissFrame

ALGORITHM_FRAMES = [
    SwissFrame
]


class GameFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.algorithm = ALGORITHM_FRAMES[0]
        self.alg_frame = self.algorithm(self)
        self.alg_frame.grid(row=0, column=0, sticky='nesw')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def change_algorithm(self, algorithm):
        self.pack_forget()
        self.algorithm = algorithm
        self.alg_frame = self.algorithm(self)
        self.alg_frame.pack(fill='both')

