import tkinter as tk

from src.player import Player


class ScoreboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(bg='#bfbfbf')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.last_pos = 0
        self.last_score = None
        self.next_row = 1

    def _add_entry(self, pos: int, name: str, score: tuple):
        font = ('Arial', 12)
        bg = '#cfcfcf' if self.next_row % 2 else '#bfbfbf'

        tk.Label(self, text=f'{pos}.', bg=bg, font=font).grid(row=self.next_row, column=0, ipady=4, sticky='nesw')
        tk.Label(self, text=name, bg=bg, font=font).grid(row=self.next_row, column=1, sticky='nesw')
        tk.Label(self, text=',  '.join(map(str, score)), bg=bg, font=font).grid(row=self.next_row, column=2, sticky='nesw')

        self.last_pos = pos
        self.last_score = score
        self.next_row += 1

    def _add_player(self, player: Player, score: tuple):
        if self.last_score == score:
            self._add_entry(self.last_pos, str(player), score)
        else:
            self._add_entry(self.last_pos + 1, str(player), score)

    def update_scoreboard(self, scoreboard: list[tuple[Player, tuple]]):
        for s in self.grid_slaves():
            s.destroy()

        self.last_pos = 0
        self.last_score = None
        self.next_row = 1

        tk.Label(self, text='Tablica Wyników', bg='#bfbfbf', font=('Arial', 18, 'bold'))\
            .grid(row=0, column=0, columnspan=3, sticky='nesw')

        for score in scoreboard:
            self._add_player(score[0], score[1])
