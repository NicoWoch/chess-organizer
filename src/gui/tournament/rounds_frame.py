import tkinter as tk
from collections.abc import Callable

from src.gui import utils
from src.algorithms.tournament import Tournament


class RoundsFrame(tk.Frame):
    FIRST_ITEM = 0
    LAST_ITEM = -1

    def __init__(self, parent, on_round_change: Callable):
        super().__init__(parent)
        self.config(bg='#bfbfbf', borderwidth=3, relief='groove')

        self.on_round_change = on_round_change
        self._buttons: dict[int, tk.Button] = {}
        self.__active_btn = 0

    @property
    def active_btn(self):
        return self.__active_btn

    @active_btn.setter
    def active_btn(self, value):
        assert -1 <= value < len(self._buttons)
        self.__active_btn = value
        self._update_btn_colors()
        self.on_round_change()

    def is_first(self):
        return self.active_btn == self.FIRST_ITEM

    def is_last(self):
        return self.active_btn == self.LAST_ITEM

    def is_round(self):
        return not self.is_first() and not self.is_last()

    def get_active_round(self):
        return self.active_btn - 1

    def update_tournament(self, tournament: Tournament):
        for btn in self._buttons.values():
            btn.destroy()

        self._buttons = {}
        self._add_btn('Zapisy', 'green_flag.png', self.FIRST_ITEM)

        for i in range(tournament.round_count):
            self._add_btn(f'Runda {i + 1}', 'white_queen.png', i + 1)

        if tournament.is_ended():
            self._add_btn('Wyniki', 'red_flag.png', self.LAST_ITEM)

        self.active_btn = self.LAST_ITEM if tournament.is_ended() else tournament.round_count

    def _add_btn(self, text: str, image_filename: str, i):
        image = utils.create_image(image_filename, (28, 28))
        btn = tk.Button(self, text=text, font=('verdana', 13), image=image, compound=tk.LEFT, command=lambda: self.__setattr__('active_btn', i))
        btn.pack(fill='x')

        self._buttons[i] = btn

    def _update_btn_colors(self):
        for btn in self._buttons.values():
            btn.config(bg='white')

        self._buttons[self.active_btn].config(bg='lightblue')


class RoundsFrameOLD(tk.Frame):
    def __init__(self, parent, on_change_round):
        super().__init__(parent)

        self.config(bg='#bfbfbf', borderwidth=3, relief='groove')

        self.buttons: list[tk.Button] = []
        self.on_change_round = on_change_round
        self.active_round_id = 0

    def set_active_round(self, round_id):
        assert 0 <= round_id < len(self.buttons), 'Invalid round'
        self.active_round_id = round_id
        self.update_btn_colors()

    def update_round_count(self, count):
        while self.buttons:
            self.buttons.pop().destroy()

        self._add_round_btn(0, 'Zapisy', 'green_flag.png')

        for _ in range(count):
            self._add_round()

        self.set_active_round(count)

    def _add_round(self):
        i = len(self.buttons)
        self._add_round_btn(i, f'Runda {i}', 'white_queen.png')

    def _add_round_btn(self, i, text, image_filename):
        text = ' ' * 2 + text

        image = utils.create_image(image_filename, (28, 28))
        btn = tk.Button(self, text=text, font=('verdana', 13), image=image, compound=tk.LEFT, command=lambda: self.change_round(i))
        btn.pack(fill='x')

        self.buttons.append(btn)

    def change_round(self, i):
        self.set_active_round(i)
        self.on_change_round()

    def update_btn_colors(self):
        for btn in self.buttons:
            btn.config(bg='white')

        self.buttons[self.active_round_id].config(bg='lightblue')
