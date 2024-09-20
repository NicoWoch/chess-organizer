import tkinter as tk

from src.gui.widgets.resizing_widgets import ResizingLabel
from src.gui.widgets.table_frame import TableFrame


class LeaderboardBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config(background="#e0c4ad")

        label = ResizingLabel(self, text="Leaderboard", relwidth=.7, maxsize=30)
        label.pack(side=tk.TOP, pady=10)

        self.table = TableFrame(self, [
            [1, 'Piotrek', 4.5, 6, 5],
            [2, 'Janusz z Polski', 3.5, 15, 13],
        ], bg='#917762')

        self.table.pack(side=tk.TOP, fill=tk.X, padx=2, pady=10)
