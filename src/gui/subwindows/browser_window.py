import tkinter as tk
from abc import ABC, abstractmethod

import src.gui.gui_utils as utils
from src.config import Config

ACTION_BAR_HEIGHT = 50


class BrowserWindow(tk.Toplevel, ABC):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x300+700+300')
        self.iconbitmap(Config.WINDOW_ICON_PATH)

        self.table = utils.Table(self, style_prefix='browser_window')
        self.table.place(x=0, y=0, relheight=1, height=-ACTION_BAR_HEIGHT, relwidth=1)

        action_bar = self.make_action_bar()
        action_bar.place(x=0, rely=1, y=-ACTION_BAR_HEIGHT, height=ACTION_BAR_HEIGHT, relwidth=1)

    @abstractmethod
    def make_action_bar(self): ...



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    BrowserWindow(root)
    root.mainloop()
