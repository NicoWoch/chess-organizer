import tkinter as tk

from src.tournament.player import Player


class PlayerWithRatingField(tk.Frame):
    def __init__(self, parent, player: Player, rating_change: float, **kwargs):
        super().__init__(parent, **kwargs)

        self.player = player
        self.rating_change = rating_change

        self.__define_layout()
        self.__setup_labels()

    def __define_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.player_label = tk.Label(self, font=('Comic Sans MS', 13))
        self.player_label.grid(row=0, column=0, sticky='e')

        self.rating_label = tk.Label(self, font=('Comic Sans MS', 10))
        self.rating_label.grid(row=0, column=1, sticky='w', padx=10)

    def __setup_labels(self):
        sign = '+' if self.rating_change >= 0 else '-'
        fg = 'green' if self.rating_change >= 0 else 'red'

        if self.rating_change != 0:
            rating_change_str = f'{sign}{abs(self.rating_change):.0f}'
        else:
            rating_change_str = ''

        self.player_label.config(text=self.player.name)
        self.rating_label.config(text=rating_change_str, fg=fg)

    def set_background(self, bg):
        self.player_label.config(bg=bg)
        self.rating_label.config(bg=bg)

    def bind_click(self, func):
        self.player_label.bind('<Button-1>', func)
        self.rating_label.bind('<Button-1>', func)

    def dynamic_swap(self, other) -> bool:
        if not isinstance(other, PlayerWithRatingField):
            return False

        self.player = other.player
        self.rating_change = other.rating_change

        self.__setup_labels()

        return True
