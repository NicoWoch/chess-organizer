import tkinter as tk
from tkinter import ttk
from typing import Callable

from src.gui.validation_utils import tk_unsigned_float_validator
from src.tournament.player import Player


class PlayerEditor(tk.Toplevel):
    def __init__(self, parent, on_edit: Callable[[Player], None], player_to_edit: Player | None = None):
        super().__init__(parent)

        self._parent_on_save = on_edit
        self._player_to_edit = player_to_edit
        self._is_edit_mode = player_to_edit is not None

        self.__setup_tk_vars()
        self.__define_layout()

        self.wait_visibility()
        self.grab_set()
        self.attributes('-topmost', True)
        self.protocol('WM_DELETE_WINDOW', lambda: (parent.lift(), parent.focus(), self.destroy()))

    def __setup_tk_vars(self):
        self.name = tk.StringVar(self, value='')
        self.rating = tk.DoubleVar(self, value=1000)

        self.name.trace_add('write', self.__parse_player_name)

        if self._is_edit_mode:
            self.name.set(self._player_to_edit.name)
            self.rating.set(self.__round_rating(self._player_to_edit.rating))

    @staticmethod
    def __round_rating(rating: float):
        return int(rating) if rating.is_integer() else round(rating, 1)

    def __define_layout(self):
        self.title('Edytuj Gracza' if self._is_edit_mode else 'Nowy Gracz')
        self.maxsize(600, 600)
        self.minsize(280, 350)
        ttk.Style().theme_use('clam')

        title = 'Edytuj Gracza' if self._is_edit_mode else 'Utwórz Gracza'
        title_label = ttk.Label(self, text=title, font=('Comic Sans MS', 22))

        name_label = ttk.Label(self, text='Imie i nazwisko:')
        name_entry = ttk.Entry(self, textvariable=self.name)
        name_entry.bind('<Return>', self._on_save, add='+')

        rating_label = ttk.Label(self, text='Ranking ELO:')
        rating_entry = ttk.Entry(self, textvariable=self.rating, **tk_unsigned_float_validator(self))
        rating_entry.bind('<Return>', self._on_save, add='+')

        save_btn_text = 'Zapisz' if self._is_edit_mode else 'Stwórz'
        save_btn = ttk.Button(self, text=save_btn_text, command=self._on_save)

        self.rowconfigure(0, weight=6)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=5)
        self.columnconfigure(0, weight=1)

        title_label.grid(row=0, column=0, pady=30)
        name_label.grid(row=1, column=0)
        name_entry.grid(row=2, column=0)
        rating_label.grid(row=3, column=0)
        rating_entry.grid(row=4, column=0)
        save_btn.grid(row=5, column=0, pady=20)

        name_entry.focus()

    def __parse_player_name(self, *_):
        self.name.set(self.name.get().title())

    def _on_save(self, *_):
        self.destroy()

        player = Player(
            name=self.name.get(),
            rating=self.rating.get(),
        )

        self._parent_on_save(player)
