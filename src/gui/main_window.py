import tkinter as tk

from src.gui.action_bar_frame import ActionBarFrame
from src.gui.tournament.tournament_frame import TournamentFrame

WINDOW_NAME = 'Chess Organizer V0.1'
WINDOW_ICON_PATH = 'images/icon.ico'
WINDOW_SIZE = 1080, 640

ALGORITHMS = []


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_NAME)
        self.iconbitmap(WINDOW_ICON_PATH)
        self.center_window()

        self.action_bar_frame = ActionBarFrame(self)
        self.action_bar_frame.grid(row=0, column=0, sticky='nesw', pady=1)

        self.tournament_frame = TournamentFrame(self)
        self.tournament_frame.grid(row=1, column=0, sticky='nesw')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)

        self.config(bg='black')

        self.make_menu()

    def center_window(self):
        top = (self.winfo_screenheight() - WINDOW_SIZE[1]) / 2
        left = (self.winfo_screenwidth() - WINDOW_SIZE[0]) / 2
        self.geometry('%dx%d+%d+%d' % (WINDOW_SIZE[0], WINDOW_SIZE[1], left, top))

    def make_menu(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)

        filemenu.add_command(label='Save', command=None)

        menubar.add_cascade(label='File', menu=filemenu)

        self.config(menu=menubar)
