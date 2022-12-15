import tkinter as tk
from collections.abc import Callable

from src.gui import utils
from src.algorithms.tournament import Tournament
from src.gui.widgets.scrollable_frame import ScrollableFrame


class RoundsFrame(tk.Frame):
    REGISTRATION = 'registration'
    RESULTS = 'results'

    def __init__(self, parent, on_round_change: Callable):
        super().__init__(parent)

        self._scroll_frame = ScrollableFrame(self, tk.Frame)
        self._buttons_frame = self._scroll_frame.child_frame
        self._buttons = {}
        self._active_button = None
        self._on_round_change = on_round_change

        self._scroll_frame.config(relief='groove', borderwidth=3)

        self._scroll_frame.place(relwidth=1, relheight=1)

    def is_registration(self) -> bool:
        return self._active_button == self.REGISTRATION

    def is_results(self) -> bool:
        return self._active_button == self.RESULTS

    def is_round(self) -> bool:
        return not self.is_registration() and not self.is_results()

    def get_active_round(self):
        assert self.is_round(), 'Tried to get round number, when no round is active'
        return self._active_button

    def set_active_btn(self, idx):
        self._buttons[self._active_button]['bg'] = 'white'
        self._buttons[idx]['bg'] = 'lightblue'

        self._active_button = idx

        self._scroll_frame.update_window()
        self._on_round_change()

    def update_tournament(self, tournament: Tournament):
        for item in self._buttons_frame.place_slaves():
            item.destroy()

        self._buttons = {}
        self._create_buttons(tournament)

        if not tournament.is_started:
            self._active_button = self.REGISTRATION
        elif tournament.is_ended:
            self._active_button = self.RESULTS
        else:
            self._active_button = tournament.round_count - 1

        self._buttons[self._active_button]['bg'] = 'lightblue'

        self._scroll_frame.update_window()
        self._on_round_change()

    def _create_buttons(self, tournament: Tournament):
        self._add_button(0, self.REGISTRATION, 'Zapisy', 'green_flag.png')

        for i in range(tournament.round_count):
            self._add_button(i + 1, i, f'Runda {i + 1}', 'white_queen.png')

        if tournament.is_ended:
            self._add_button(tournament.round_count + 1, self.RESULTS, 'Wyniki', 'red_flag.png')

        btn_count = tournament.round_count + tournament.is_ended + 1
        btn_height = 50
        self._scroll_frame.height = btn_height * btn_count + 6

    def _add_button(self, i, idx, text: str, image_path: str):
        image = utils.create_image(image_path, (28, 28))
        btn = tk.Button(self._buttons_frame, text=text, font='verdana 13', image=image, bg='white', height=20,
                        compound=tk.LEFT, command=lambda: self.set_active_btn(idx))
        btn.place(y=i * 50, relwidth=1, width=-10, height=50)
        self._buttons[idx] = btn
