import tkinter as tk
from abc import ABC, abstractmethod

from src.gui import utils
from src.gui.widgets.table import Table

ACTION_BAR_HEIGHT = 50


class BrowserWindow(tk.Toplevel, ABC):
    def __init__(self, parent):
        super().__init__(parent)

        utils.add_icon(self)

        self.table = Table(self)
        self.table.style['header']['font'] = 'Arial 18'
        self.table.style['header']['height'] = 35
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
