import tkinter as tk
from abc import ABC, abstractmethod
from typing import Any

from src.gui import utils
from src.gui.widgets.table import Table, ScrollableTableFrame

ACTION_BAR_HEIGHT = 50

BROWSER_TABLE_STYLE = {
    'header_height': 40,
    'row_height': 30,
    'header_bg': '#d5d5d5',
    'row_bg': '#f4f4f4',
    'odd_row_bg': '#e0e0e0',
    'selected_bg': '#6ebcf4',
    'font': ('Arial', 12),
    'header_font': ('Comic Sans MS', 14),
}


class BrowserWindow(tk.Toplevel, ABC):
    def __init__(self, parent):
        super().__init__(parent)
        utils.add_icon(self)

        table_style = BROWSER_TABLE_STYLE.copy()
        self.modify_style(table_style)

        scrollable_table = ScrollableTableFrame(self)

        self.table = scrollable_table.table
        self.table.change_table_style(table_style)
        action_bar = self.make_action_bar()

        scrollable_table.place(x=0, y=0, relheight=1, height=-ACTION_BAR_HEIGHT, relwidth=1)
        action_bar.place(x=0, rely=1, y=-ACTION_BAR_HEIGHT, height=ACTION_BAR_HEIGHT, relwidth=1)

    @classmethod
    def modify_style(cls, style: dict[str, Any]):
        pass

    @abstractmethod
    def make_action_bar(self): ...


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    BrowserWindow(root)
    root.mainloop()
