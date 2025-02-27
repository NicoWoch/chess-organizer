import tkinter as tk
from typing import Callable

from src.player import Player, Gender
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
        self.gender = tk.StringVar(value=str(player.gender.value))
        self.rating = tk.IntVar(value=player.rating)

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
        self.make_entry(main_frame, 3, 'Ranking', self.rating)

        tk.Button(main_frame, text='Zapisz', command=self.save, height=2) \
            .grid(row=4, column=0, columnspan=2, pady=10, sticky='nesw')

        main_frame.place(x=15, y=15, relwidth=1, width=-30, relheight=1, height=-30)

    @classmethod
    def make_entry(cls, main_frame: tk.Frame, i: int, label: str, var: tk.Variable, bind=None):
        tk.Label(main_frame, text=label)\
            .grid(row=i, column=0)

        entry = tk.Entry(main_frame, textvariable=var)
        entry.grid(row=i, column=1)

        if bind is not None:
            entry.bind('<KeyRelease>', bind)

    def update_player_label(self, *_):
        self.player_label.set(f'Gracz {self.name.get()} {self.surname.get()}')

    def save(self, *_):
        self.player.name = self.name.get()
        self.player.surname = self.surname.get()
        self.player.gender = Gender(self.gender.get())
        self.player.rating = self.rating.get()

        self.on_save()
        self.destroy()


def _test_window():
    root = tk.Tk()
    root.geometry('1x1+0+0')
    editor = PlayerEditorWindow(root, Player.create_player(
        name='adam', surname='nowak', rating=1000, group_name='default', gender=Gender.Men
    ), lambda: 0)
    editor.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
    root.mainloop()


if __name__ == '__main__':
    _test_window()
