import tkinter as tk
from typing import Callable

from src.config import Config
from src.gui.subwindows.info.error_window import WindowException
from src.player import Player
from src.gui import utils


class PlayerEditorWindow(tk.Toplevel):
    def __init__(self, parent, player: Player, on_save: Callable):
        super().__init__(parent)

        self.title('Gracz')
        utils.add_icon(self)
        utils.center_window(self, (280, 250))
        self.resizable(False, False)

        self.player = player
        self.on_save = on_save

        self.player_label = tk.StringVar()
        self.name = tk.StringVar(value=player.name)
        self.surname = tk.StringVar(value=player.surname)
        self.rating = tk.StringVar(value=str(player.rating))

        self.update_player_label()
        self.make_main_frame()

    def make_main_frame(self):
        main_frame = tk.Frame(self)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        for i in range(5):
            main_frame.grid_rowconfigure(i, weight=1)

        tk.Label(main_frame, textvariable=self.player_label).grid(row=0, column=0, columnspan=2, pady=10)

        self.make_entry(main_frame, 1, 'Imie', self.name, bind=self.update_player_label)
        self.make_entry(main_frame, 2, 'Nazwisko', self.surname, bind=self.update_player_label)
        self.make_entry(main_frame, 3, 'Ranking', self.rating, validate=self.__rating_validator)

        tk.Button(main_frame, text='Zapisz', command=self.save, height=2) \
            .grid(row=4, column=0, columnspan=2, pady=10, sticky='nesw')

        main_frame.place(x=15, y=15, relwidth=1, width=-30, relheight=1, height=-30)

    def make_entry(self, main_frame: tk.Frame, i: int, label: str, var: tk.Variable, bind=None, validate=None):
        tk.Label(main_frame, text=label) \
            .grid(row=i, column=0)

        entry = tk.Entry(main_frame, textvariable=var)
        entry.grid(row=i, column=1)

        if bind is not None:
            entry.bind('<KeyRelease>', bind)

        if validate is not None:
            entry.configure(validate='all', validatecommand=(self.register(validate), '%P'))

    @classmethod
    def __rating_validator(cls, text: str) -> bool:
        return text == '' or text.isdigit()

    def update_player_label(self, *_):
        self.player_label.set(f'Gracz {self.name.get()} {self.surname.get()}')

    def save(self, *_):
        name = self.name.get().strip().title()
        surname = self.surname.get().strip().title()

        if name == '' or surname == '':
            return

        if self.rating.get() == '':
            return

        rating = int(self.rating.get())

        if rating < 10 or rating > 10_000:
            raise WindowException(Config.Messages.RATING_OVERFLOW)

        self.player.name = name
        self.player.surname = surname
        self.player.rating = rating

        self.on_save()
        self.destroy()


def _test_window():
    root = tk.Tk()
    root.geometry('1x1+0+0')
    editor = PlayerEditorWindow(root, Player.create_player(
        name='adam', surname='nowak', rating=1000
    ), lambda: 0)
    editor.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
    root.mainloop()


if __name__ == '__main__':
    _test_window()
