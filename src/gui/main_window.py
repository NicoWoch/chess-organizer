import logging
import tkinter as tk
import traceback

from src import dummy_generator
from src.algorithms.game import Result
from src.config import Config
from src.db import MainDB
from src.gui import utils
from src.gui.action_bar_frame import ActionBarFrame
from src.gui.subwindows.info.about_window import AboutWindow
from src.gui.subwindows.info.error_window import ErrorWindow, WindowException
from src.gui.subwindows.info.license_window import LicenseWindow
from src.gui.tournament.tournament_frame import TournamentFrame


def show_error(self, exc, val, tb):
    if isinstance(val, AssertionError) and len(val.args) == 1 and isinstance(val.args[0], WindowException):
        logging.warning(f'WindowError: {val.args[0]}')
        ErrorWindow(self, val.args[0]).mainloop()
    else:
        err_str = f'Raised "{exc.__name__}": {val}\n' \
                  f'--- Traceback ---\n' + ''.join(traceback.format_exception(exc, val, tb))

        ErrorWindow(self, WindowException(f'Unhandled {exc.__name__} error\n"{val}"')).mainloop()

        logging.error(err_str)
        print(err_str)

tk.Tk.report_callback_exception = show_error

DEV_KEYS = list('devon\r')


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(Config.WINDOW_NAME)
        self.iconbitmap(Config.WINDOW_ICON_PATH)
        utils.center_window(self, Config.WINDOW_SIZE)
        self.minsize(900, 400)

        self.tournament_frame = TournamentFrame(self, self._register_subwindow)
        self.action_bar_frame = ActionBarFrame(self, self.tournament_frame)
        self.subwindows = []

        self.action_bar_frame.grid(row=0, column=0, sticky='nesw', pady=1)
        self.tournament_frame.grid(row=1, column=0, sticky='nesw')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)

        self.config(bg='black')

        self.make_menu()

        self._keys = []
        self.bind('<Button-1>', self._remove_subwindows)
        self.bind('<Key>', self._on_key_pressed)
        self.bind('<Key-F11>', self._enable_fullscreen_mode)
        self.bind('<Key-Escape>', self._disable_fullscreen_mode)

    def _remove_subwindows(self, *_):
        for x in self.subwindows:
            x.destroy()

        self.subwindows.clear()

    def _register_subwindow(self, window):
        self.subwindows.append(window)

    def center_window(self):
        top = (self.winfo_screenheight() - Config.WINDOW_SIZE[1]) / 2
        left = (self.winfo_screenwidth() - Config.WINDOW_SIZE[0]) / 2
        self.geometry('%dx%d+%d+%d' % (Config.WINDOW_SIZE[0], Config.WINDOW_SIZE[1], left, top))

    def make_menu(self, *, empty_menu=False, dev=False):
        menubar = tk.Menu(self)

        if empty_menu:
            self.config(menu=menubar)
            return

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Stwórz turniej', command=lambda: self.tournament_frame.browse_tournaments(create=True))
        file_menu.add_command(label='Przeglądaj turnieje', command=lambda: self.tournament_frame.browse_tournaments())
        file_menu.add_command(label='Zamknij turniej', command=self.tournament_frame.close_tournament)
        menubar.add_cascade(label='Plik', menu=file_menu)

        player_menu = tk.Menu(menubar, tearoff=0)
        player_menu.add_command(label='Przeglądaj graczy',  command=lambda: self.tournament_frame.browse_players())
        player_menu.add_command(label='Usuń graczy',        command=self.tournament_frame.remove_players)
        menubar.add_cascade(label='Gracz', menu=player_menu)

        tournament_menu = tk.Menu(menubar, tearoff=0)
        set_result_menu = tk.Menu(tournament_menu, tearoff=0)
        set_result_menu.add_command(label='Biały wygrał',  command=lambda: self.tournament_frame.set_result(Result.White))
        set_result_menu.add_command(label='Czarny wygrał', command=lambda: self.tournament_frame.set_result(Result.Black))
        set_result_menu.add_command(label='Remis',         command=lambda: self.tournament_frame.set_result(Result.Draw))
        set_result_menu.add_command(label='Jeszcze grają', command=lambda: self.tournament_frame.set_result(Result.Playing))
        tournament_menu.add_cascade(label='Wynik', menu=set_result_menu)
        tournament_menu.add_command(label='Następna runda',        command=self.tournament_frame.next_round)
        tournament_menu.add_command(label='Zakończ turniej',  command=self.tournament_frame.end_tournament)
        menubar.add_cascade(label='Turniej', menu=tournament_menu)

        print_menu = tk.Menu(menubar, tearoff=0)
        print_menu.add_command(label='Drukuj listę startową', command=lambda: self.tournament_frame.make_pdf_starting_list('print'))
        print_menu.add_command(label='Drukuj parowanie', command=lambda: self.tournament_frame.make_pdf_active_pairings('print'))
        print_menu.add_command(label='Drukuj wyniki', command=lambda: self.tournament_frame.make_pdf_results('print'))
        print_menu.add_command(label='Zapisz listę startową', command=lambda: self.tournament_frame.make_pdf_starting_list('save'))
        print_menu.add_command(label='Zapisz parowanie', command=lambda: self.tournament_frame.make_pdf_active_pairings('save'))
        print_menu.add_command(label='Zapisz wyniki', command=lambda: self.tournament_frame.make_pdf_results('save'))
        menubar.add_cascade(label='Drukowanie', menu=print_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        # help_menu.add_command(label='Sprawdź aktualizacje', command=lambda: print('COMMING SOON'), state=tk.DISABLED)
        help_menu.add_command(label='O programie', command=self._show_window_cmd(AboutWindow, self))
        help_menu.add_command(label='Licencja', command=self._show_window_cmd(LicenseWindow, self))
        menubar.add_cascade(label='Pomoc', menu=help_menu)

        if dev:
            self.make_dev_menu(menubar)

        self.config(menu=menubar)

    def _show_window_cmd(self, win_func, *args, **kwargs):
        return lambda: self.subwindows.append(win_func(*args, **kwargs))

    def _enable_fullscreen_mode(self, *_):
        self.attributes('-fullscreen', True)
        self.make_menu(empty_menu=True)

    def _disable_fullscreen_mode(self, *_):
        self.attributes('-fullscreen', False)
        self.make_menu()

    def _show_dev_menu(self):
        self.make_menu(dev=True)

    def _on_key_pressed(self, event):
        self._keys.append(event.char)

        while len(self._keys) > len(DEV_KEYS):
            self._keys.pop(0)

        if self._keys == DEV_KEYS:
            logging.info('DEVELOPER MODE - ON')
            self.make_menu(dev=True)

    def make_dev_menu(self, menubar):
        devmenu = tk.Menu(menubar, tearoff=0)

        for func_name in dir(self):
            func = getattr(self, func_name)

            if func_name.startswith('_dev_') and callable(func):
                display_name = func_name[5:].replace('_', ' ').title()

                devmenu.add_command(label=display_name, command=func)

        menubar.add_cascade(label='Developer', menu=devmenu)

    def _dev_hide_menu(self):
        logging.info('DEVELOPER MODE - OFF')
        self.make_menu()

    def _dev_create_5_random_players(self):
        dummy_players = dummy_generator.get_random_players(5)
        MainDB.save_players(MainDB.load_players() + dummy_players)

    def _dev_create_15_random_players(self):
        dummy_players = dummy_generator.get_random_players(15)
        MainDB.save_players(MainDB.load_players() + dummy_players)

    def _dev_clear_players(self):
        MainDB.save_players([])

    def _dev_create_dummy_tournament(self):
        tournaments = MainDB.load_tournaments()
        tournaments.append(dummy_generator.create_empty_tournament(len(tournaments)))
        MainDB.save_tournaments(tournaments)

    def _dev_create_3_dummy_tournaments(self):
        tournaments = MainDB.load_tournaments()

        for _ in range(3):
            tournaments.append(dummy_generator.create_empty_tournament(len(tournaments)))

        MainDB.save_tournaments(tournaments)

    def _dev_clear_tournaments(self):
        MainDB.save_tournaments([])
