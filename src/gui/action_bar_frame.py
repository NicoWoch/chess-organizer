import tkinter as tk


class FunctionsFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = tk.Label(self, text='Functions Bar')
        self.label.pack()

        self.config(bg='blue')
