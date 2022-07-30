import tkinter as tk


class ScoreboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = tk.Label(self, text='hi')
        self.label.grid()

        self.config(padx=20, pady=20, bg='#bfbfbf')
