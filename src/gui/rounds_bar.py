import itertools
import tkinter as tk

from src.gui.widgets.resizing_widgets import ResizingLabel, ResizingButton
from src.tournament.interactive_tournament import InteractiveTournament


class RoundsBar(tk.Frame):
    def __init__(self, parent, on_page_change):
        super().__init__(parent)

        self.config(bg='#e0c4ad')

        self.on_page_change = on_page_change

        self._label = ResizingLabel(self, relwidth=.7, maxsize=30)
        self._label.pack()

        self._buttons = []
        self._pages = []
        self._pages_types = []

        self._selected = None
        self._last_selected_sent = None

        self.update_tournament_pages(None)

    def update_tournament_pages(self, tournament: InteractiveTournament | None):
        if tournament is None:
            pages = []
            pages_types = []
            title = 'brak otwartego\nturnieju'
        else:
            pages = [
                'Lista Startowa',
                *(f'Runda {i + 1}' for i in range(tournament.round_count)),
                *(['Wyniki'] if tournament.is_finished() else []),
            ]
            pages_types = [
                1, *([0] * tournament.round_count),
                *([1] if tournament.is_finished() else []),
            ]

            if not tournament.is_running():
                title = 'Zapisy'
            elif tournament.is_running():
                title = f'Runda {tournament.round_count}'
            else:
                title = 'Koniec'

        print(pages)
        self._update_pages(pages, pages_types, title)

    def _update_pages(self, pages: list[str], pages_types: list[int], title: str):
        self._pages = pages
        self._pages_types = pages_types
        self.__update_buttons()
        self._label.config(text=title)

    def __update_buttons(self):
        correct_pages = (self.__is_correct_btn(i) for i, _ in enumerate(self._buttons))
        correct = len(list(itertools.takewhile(lambda x: x, correct_pages)))

        for _ in range(len(self._buttons) - correct):
            self.__remove_last_button()

        for i, title in enumerate(self._pages[correct:], start=correct):
            self.__add_button_at_end(title, i)

    def __is_correct_btn(self, btn_id: int) -> bool:
        if btn_id >= len(self._buttons) or btn_id >= len(self._pages):
            return False

        return self._buttons[btn_id]['text'] == self._pages[btn_id] and \
            self._buttons[btn_id].btn_type == self._pages_types[btn_id]

    def __add_button_at_end(self, title: str, index: int):
        btn = ResizingButton(self, text=title, activebackground='#692c03', relwidth=.8, maxsize=15, borderwidth=0,
                             command=lambda *_: self.select(index))
        btn.btn_type = self._pages_types[index]

        self._buttons.append(btn)
        self.__deselect_button(index)

        btn.pack(fill=tk.X, padx=5, pady=1)

    def __remove_last_button(self):
        self._buttons[-1].pack_forget()
        self._buttons[-1].destroy()
        self._buttons.pop()

    def __select_button(self, i: int):
        self._buttons[i].config(relief=tk.SUNKEN, borderwidth=4)

    def __deselect_button(self, i: int):
        bg = {
            0: '#917762',
            1: '#634d3e',
        }[self._pages_types[i]]

        self._buttons[i].config(bg=bg, relief=tk.FLAT, borderwidth=4)

    def select(self, index: int):

        if len(self._buttons) == 0:
            self._selected = None
        elif self._selected != index % len(self._pages):
            if self._selected is not None:
                self.__deselect_button(self._selected)

            self.__select_button(index)
            self._selected = index % len(self._pages)

        self.__on_page_change_with_repeat_check()

    def __on_page_change_with_repeat_check(self):
        if self._last_selected_sent == self._selected:
            print('repeat :(')  # TODO: i cannot cache this, so remove this function and directly call on_page_change
            return

        self.on_page_change(self._selected)
        self._last_selected_sent = self._selected
