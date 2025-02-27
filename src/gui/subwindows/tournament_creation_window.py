import tkinter as tk
from collections import namedtuple
from typing import Callable

from src.algorithms.swiss_tournament import SwissTournament
from src.config import Config
from src.gui import utils

Alg = namedtuple('Alg', ('name', 'cls'))

ALGORITHMS = [
    Alg('Swiss', SwissTournament),
]


class TournamentCreationWindow(tk.Toplevel):
    def __init__(self, parent, on_create: Callable):
        super().__init__(parent)

        self.title('Stwóz turniej')
        utils.add_icon(self)
        utils.center_window(self, (300, 180))
        self.resizable(False, False)

        self.on_create = on_create
        self.name = tk.StringVar()
        self.algorithm = tk.StringVar(value=ALGORITHMS[0].name)

        self.make_main_frame()

    def make_main_frame(self):
        main_frame = tk.Frame(self)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        for i in range(3):
            main_frame.grid_rowconfigure(i, weight=1)

        tk.Label(main_frame, text='Nazwa turnieju') \
            .grid(row=0, column=0, pady=0)
        tk.Entry(main_frame, textvariable=self.name) \
            .grid(row=0, column=1, pady=5)
        tk.Label(main_frame, text='Algorytm') \
            .grid(row=1, column=0, pady=0)
        tk.OptionMenu(main_frame, self.algorithm, *[alg.name for alg in ALGORITHMS]) \
            .grid(row=1, column=1, pady=5)
        tk.Button(main_frame, text='Utwórz turniej', command=self._create, height=2) \
            .grid(row=2, column=0, columnspan=2, pady=10)

        main_frame.place(x=15, y=15, relwidth=1, width=-30, relheight=1, height=-30)

    def _create(self, *_):
        alg_class = next(alg.cls for alg in ALGORITHMS if alg.name == self.algorithm.get())
        self.on_create(alg_class(self.name.get()))
        self.destroy()



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    TournamentCreationWindow(root, lambda **x: print(x))
    root.mainloop()
