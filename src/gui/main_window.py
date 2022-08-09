import logging
import random
import tkinter as tk
import traceback

from src import dummy_generator
from src.config import Config
from src.db import MainDB
from src.gui.action_bar_frame import ActionBarFrame
from src.gui.subwindows.error_window import ErrorWindow, WindowException
from src.gui.tournament.tournament_frame import TournamentFrame


def show_error(self, exc, val, tb):
    if isinstance(val, AssertionError) and isinstance(val.args[0], WindowException):
        logging.warning(f'WindowError: {val.args[0]}')
        ErrorWindow(self, val.args[0]).mainloop()
    else:
        err_id = random.randint(0, 99)
        err_str = f'Raised "{exc.__name__}" <{err_id}>: {val}'
        tb_str = f'TRACEBACK: "{exc.__name__}" <{err_id}>: {val}\n\n' + ''.join(traceback.format_exception(exc, val, tb)) + '\n\n\n'

        with open(Config.LOG_TB_FILE, 'a') as f:
            f.write(tb_str)

        logging.error(err_str)
        print(err_str)

tk.Tk.report_callback_exception = show_error

DEV_KEYS = list('devon\r')


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(Config.WINDOW_NAME)
        self.iconbitmap(Config.WINDOW_ICON_PATH)

        self.tournament_frame = TournamentFrame(self)
        self.action_bar_frame = ActionBarFrame(self, self.tournament_frame)

        self.action_bar_frame.grid(row=0, column=0, sticky='nesw', pady=1)
        self.tournament_frame.grid(row=1, column=0, sticky='nesw')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)

        self.config(bg='black')

        self.make_menu()

        self.center_window()

        self._keys = []
        self.bind('<Key>', self._on_key_pressed)
        self.bind('<Key-F11>', self._enable_fullscreen_mode)
        self.bind('<Key-Escape>', self._disable_fullscreen_mode)

    def center_window(self):
        top = (self.winfo_screenheight() - Config.WINDOW_SIZE[1]) / 2
        left = (self.winfo_screenwidth() - Config.WINDOW_SIZE[0]) / 2
        self.geometry('%dx%d+%d+%d' % (Config.WINDOW_SIZE[0], Config.WINDOW_SIZE[1], left, top))

    def make_menu(self, dev=False):
        menubar = tk.Menu(self)

        if dev:
            devmenu = tk.Menu(menubar, tearoff=0)

            for func_name in dir(self):
                func = getattr(self, func_name)

                if func_name.startswith('_dev_') and callable(func):
                    display_name = func_name[5:].replace('_', ' ').title()

                    devmenu.add_command(label=display_name, command=func)

            menubar.add_cascade(label='Developer', menu=devmenu)

        self.config(menu=menubar)

    def _enable_fullscreen_mode(self, *_):
        self.attributes('-fullscreen', True)

    def _disable_fullscreen_mode(self, *_):
        self.attributes('-fullscreen', False)

    def _show_dev_menu(self):
        self.make_menu(dev=True)

    def _on_key_pressed(self, event):
        self._keys.append(event.char)

        while len(self._keys) > len(DEV_KEYS):
            self._keys.pop(0)

        if self._keys == DEV_KEYS:
            logging.info('DEVELOPER MODE - ON')
            self.make_menu(dev=True)

    def _dev_hide_menu(self):
        logging.info('DEVELOPER MODE - OFF')
        self.make_menu()

    def _dev_create_5_random_players(self):
        dummy_players = dummy_generator.get_random_players(5)
        MainDB.save_players(MainDB.load_players() + dummy_players)

    def _dev_clear_players(self):
        MainDB.save_players([])

    def _dev_create_dummy_tournament(self):
        tournaments = MainDB.load_tournaments()
        tournaments.append(dummy_generator.create_empty_tournament(len(tournaments)))
        MainDB.save_tournaments(tournaments)

    def _dev_clear_tournaments(self):
        MainDB.save_tournaments([])
