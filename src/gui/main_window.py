import tkinter as tk

from src.gui.action_bar_frame import ActionBarFrame
from src.gui.game_frame import GameFrame

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
        self.action_bar_frame.grid(row=0, column=0, sticky='nesw')

        self.game_frame = GameFrame(self)
        self.game_frame.grid(row=1, column=0, sticky='nesw')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)

        self.columnconfigure(0, weight=1)

    def center_window(self):
        top = (self.winfo_screenheight() - WINDOW_SIZE[1]) / 2
        left = (self.winfo_screenwidth() - WINDOW_SIZE[0]) / 2
        self.geometry('%dx%d+%d+%d' % (WINDOW_SIZE[0], WINDOW_SIZE[1], left, top))
