import logging
import random
import tkinter as tk
import traceback

from src.gui.action_bar_frame import ActionBarFrame
from src.gui.tournament.tournament_frame import TournamentFrame
from src.config import Config


def show_error(_, exc: type, val, tb):
    err_id = random.randint(0, 99)
    err_str = f'Raised "{exc.__name__}" <{err_id}>: {val}'
    tb_str = f'TRACEBACK: "{exc.__name__}" <{err_id}>: {val}\n\n' + ''.join(traceback.format_exception(exc, val, tb)) + '\n\n\n'

    with open(Config.LOG_TB_FILE, 'a') as f:
        f.write(tb_str)

    logging.error(err_str)
    print(err_str)

tk.Tk.report_callback_exception = show_error


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

    def center_window(self):
        top = (self.winfo_screenheight() - Config.WINDOW_SIZE[1]) / 2
        left = (self.winfo_screenwidth() - Config.WINDOW_SIZE[0]) / 2
        self.geometry('%dx%d+%d+%d' % (Config.WINDOW_SIZE[0], Config.WINDOW_SIZE[1], left, top))

    def make_menu(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)

        filemenu.add_command(label='Function 1', command=self.dev_function_1)

        menubar.add_cascade(label='Developer', menu=filemenu)

        self.config(menu=menubar)

    def dev_function_1(self):
        self.tournament_frame.rounds_frame.update_btn_colors()
