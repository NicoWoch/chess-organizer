import tkinter as tk
from abc import ABC, abstractmethod

from src.config import Config
from src.gui.widgets.table import Table

ACTION_BAR_HEIGHT = 50


class BrowserWindow(tk.Toplevel, ABC):
    def __init__(self, parent):
        super().__init__(parent)

        self.iconbitmap(Config.WINDOW_ICON_PATH)

        self.table = Table(self)
        self.table.header_fontsize = 18
        self.table.place(x=0, y=0, relheight=1, height=-ACTION_BAR_HEIGHT, relwidth=1)

        action_bar = self.make_action_bar()
        action_bar.place(x=0, rely=1, y=-ACTION_BAR_HEIGHT, height=ACTION_BAR_HEIGHT, relwidth=1)

        self.bind('<Control-a>', lambda *_: self.table.select_all())
        self.bind('<Control-d>', lambda *_: self.table.remove_selection())

    @abstractmethod
    def make_action_bar(self): ...



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    BrowserWindow(root)
    root.mainloop()
