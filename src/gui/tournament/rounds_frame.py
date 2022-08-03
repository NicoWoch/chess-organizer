import tkinter as tk
from typing import List

import src.gui.gui_utils as utils


class RoundsFrame(tk.Frame):
    def __init__(self, parent, on_change_round):
        super().__init__(parent)

        self.config(bg='#bfbfbf', borderwidth=3, relief='groove')

        self.buttons: List[tk.Button] = []
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
