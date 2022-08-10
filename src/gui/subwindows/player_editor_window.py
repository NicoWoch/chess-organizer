import tkinter as tk
from typing import Callable

from src.config import Config
from src.player import Player, Gender
import src.gui.gui_utils as utils


class PlayerEditorWindow(tk.Toplevel):
    def __init__(self, parent, player: Player, on_save: Callable):
        super().__init__(parent)

        self.title('Gracz')
        self.iconbitmap(Config.WINDOW_ICON_PATH)
        utils.center_window(self, (210, 250))

        self.player = player
        self.on_save = on_save

        self.player_label = tk.StringVar()
        self.name = tk.StringVar(value=player.name)
        self.surname = tk.StringVar(value=player.surname)
        self.gender = tk.StringVar(value=player.gender.value)
        self.rating = tk.IntVar(value=player.rating)
        self.title = tk.StringVar(value=player.title)

        self.update_player_label()
        self.make_main_frame()

    def make_main_frame(self):
        main_frame = tk.Frame(self)

        tk.Label(main_frame, textvariable=self.player_label).grid(row=0, column=0, columnspan=2, pady=10)

        self.make_entry(main_frame, 1, 'Imie', self.name, bind=self.update_player_label)
        self.make_entry(main_frame, 2, 'Nazwisko', self.surname, bind=self.update_player_label)
        self.make_option_menu(main_frame, 3, 'Płeć', self.gender, [x.value for x in Gender])
        self.make_entry(main_frame, 4, 'Ranking', self.rating)
        self.make_entry(main_frame, 5, 'Tytuł', self.title)

        tk.Button(main_frame, text='Zapisz', command=self.save, height=2)\
            .grid(row=6, column=0, columnspan=2, pady=10, sticky='nesw')

        main_frame.pack(fill='both', padx=15, pady=15)

    def make_entry(self, main_frame, i, label, var, bind=None):
        tk.Label(main_frame, text=label)\
            .grid(row=i, column=0)

        entry = tk.Entry(main_frame, textvariable=var)
        entry.grid(row=i, column=1)

        if bind is not None:
            entry.bind('<KeyRelease>', bind)

    def make_option_menu(self, main_frame, i, label, var, options):
        tk.Label(main_frame, text=label)\
            .grid(row=i, column=0)
        tk.OptionMenu(main_frame, var, *options)\
            .grid(row=i, column=1)

    def update_player_label(self, *_):
        self.player_label.set(f'Gracz {self.name.get()} {self.surname.get()}')

    def save(self, *_):
        self.player.name = self.name.get()
        self.player.surname = self.surname.get()
        self.player.gender = Gender(self.gender.get())
        self.player.rating = self.rating.get()
        self.player.title = self.title.get()

        self.on_save()
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    PlayerEditorWindow(root, Player.create_player(name='adam', surname='nowak', rating=1000, group_name='default', gender=Gender.Men), lambda: 0)
    root.mainloop()
