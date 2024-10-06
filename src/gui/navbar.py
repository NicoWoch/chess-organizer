import tkinter as tk
from abc import ABC, abstractmethod
from PIL import ImageTk, Image
from tktooltip import ToolTip

from src.gui.widgets.tkinter_image import TkinterImage
from src.tournament.round import GameResult


class NavbarListener(ABC):
    @abstractmethod
    def show_tournament_explorer(self): ...

    @abstractmethod
    def show_tournament_creator(self): ...

    @abstractmethod
    def show_players_explorer(self): ...

    @abstractmethod
    def show_tournament_data(self): ...

    @abstractmethod
    def next_round(self): ...

    @abstractmethod
    def remove_last_round(self): ...

    @abstractmethod
    def finish(self): ...

    @abstractmethod
    def set_selected_result(self, result: GameResult | None): ...

    @abstractmethod
    def edit_pairing(self): ...


class Navbar(tk.Frame):
    def __init__(self, parent, *, listener: NavbarListener):
        super().__init__(parent)

        self.config(background="#522E1C")

        self.images = []

        self.configure_grid(13)

        self.add_button('tournament.png', 0, listener.show_tournament_creator, 'Nowy Turniej')
        self.add_button('finished_tournament.png', 1, listener.show_tournament_explorer,
                        'Pokaż Wszystkie Turnieje')

        self.add_button('white_won.png', 5, lambda: listener.set_selected_result(GameResult.WIN))
        self.add_button('draw_1.png', 6, lambda: listener.set_selected_result(GameResult.DRAW))
        self.add_button('black_won.png', 7, lambda: listener.set_selected_result(GameResult.LOSE))

        self.add_button('players.png', 11, listener.show_players_explorer, 'Pokaż Wszystkich Graczy')
        self.add_button('players.png', 12, listener.show_players_explorer, 'Pokaż Wszystkich Graczy')

        self.__define_menu(listener)

        # btn = tk.Button(self, text="SHOW TOURNAMENTS", command=listener.show_tournament_explorer)
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="NEW TOURNAMENT", command=listener.show_tournament_creator)
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="NEXT ROUND", command=listener.next_round)
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="REMOVE LAST ROUND", command=listener.remove_last_round)
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="WHITE WIN", bg='green',
        #                 command=lambda: listener.set_selected_result(GameResult.WIN))
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="DRAW", bg='green', command=lambda: listener.set_selected_result(GameResult.DRAW))
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="WHITE LOST", bg='green',
        #                 command=lambda: listener.set_selected_result(GameResult.LOSE))
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="CLEAR RESULT", bg='green', command=lambda: listener.set_selected_result(None))
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="EDIT PAIRING", command=listener.edit_pairing)
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="FINISH", command=listener.finish)
        # btn.pack(side=tk.LEFT)
        # btn = tk.Button(self, text="SHOW PLAYERS", command=listener.show_players_explorer)
        # btn.pack(side=tk.LEFT)

    def configure_grid(self, no_columns: int):
        self.grid_rowconfigure(0, weight=1)

        for i in range(no_columns):
            self.grid_columnconfigure(i, weight=1)

    def add_button(self, image_path, column, command, tooltip=None):
        image = TkinterImage.open(image_path, 64)

        btn = tk.Button(self, image=image, command=command, bg=self.cget('bg'), borderwidth=0,
                        highlightthickness=0, activebackground='#B5AB79')
        btn.grid(row=0, column=column, padx=4, pady=4)

        if tooltip is not None:
            ToolTip(btn, msg=tooltip, follow=False, delay=2.0)

    def __define_menu(self, listener: NavbarListener):
        menubar = tk.Menu(self.winfo_toplevel(), font='Arial 10 italic', bg='#421E0C', bd=0, activebackground='#B5AB79')

        menu_control = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='  Zarządzanie  ', menu=menu_control)

        menu_control.add_command(label='Nowy Turniej', command=listener.show_tournament_creator)
        menu_control.add_command(label='Wszystkie Turnieje', command=listener.show_tournament_explorer)
        menu_control.add_command(label='Wszyscy Gracze', command=listener.show_players_explorer)

        menu_tr = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='  Turniej  ', menu=menu_tr)

        menu_tr.add_command(label='Następna Runda', command=listener.next_round)
        menu_tr.add_command(label='Usuń Ostatnią Rundę', command=listener.remove_last_round)
        menu_tr.add_command(label='Edytuj Parowanie', command=listener.edit_pairing)
        menu_tr.add_command(label='Zakończ Turniej', command=listener.finish)
        menu_tr.add_command(label='Pokaż Dane Turnieju', command=listener.show_tournament_data)

        menu_result = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='  Wynik  ', menu=menu_result)

        menu_result.add_command(label='Biały Wygrał', command=lambda: listener.set_selected_result(GameResult.WIN))
        menu_result.add_command(label='Remis', command=lambda: listener.set_selected_result(GameResult.DRAW))
        menu_result.add_command(label='Czarny Wygrał', command=lambda: listener.set_selected_result(GameResult.LOSE))
        menu_result.add_command(label='Brak Wyniku', command=lambda: listener.set_selected_result(None))

        self.winfo_toplevel().config(menu=menubar)
