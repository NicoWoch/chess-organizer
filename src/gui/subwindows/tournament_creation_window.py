import tkinter as tk
from collections import namedtuple
from typing import Callable

from src.algorithms.random_tournament import RandomTournament
from src.algorithms.swiss_tournament import SwissTournament
from src.config import Config

Alg = namedtuple('Alg', ('name', 'cls'))

ALGORITHMS = [
    Alg('Swiss', SwissTournament),
    Alg('Random', RandomTournament)
]


class TournamentCreationWindow(tk.Toplevel):
    def __init__(self, parent, on_create: Callable):
        super().__init__(parent)

        self.title('Stwóz turniej')
        self.geometry('+500+500')
        self.iconbitmap(Config.WINDOW_ICON_PATH)

        self.on_create = on_create
        self.name = tk.StringVar()
        self.algorithm = tk.StringVar(value=ALGORITHMS[0].name)

        self.make_main_frame()

    def make_main_frame(self):
        main_frame = tk.Frame(self)

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

        main_frame.pack(fill='both', padx=15, pady=15)

    def _create(self, *_):
        alg_class = next(alg.cls for alg in ALGORITHMS if alg.name == self.algorithm.get())
        self.on_create(alg_class(self.name.get(), []))
        self.destroy()



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    TournamentCreationWindow(root, lambda **x: print(x))
    root.mainloop()
