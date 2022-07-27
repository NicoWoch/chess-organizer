import tkinter as tk
from tkinter import ttk


class PairsFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        column_names = ('NB', 'WHITE', 'BLACK', 'POINTS')
        column_sizes = (20, 300, 300, 80)

        self.tree = ttk.Treeview(self, columns=column_names, show='headings', height=10)

        for name, size in zip(column_names, column_sizes):
            self.tree.heading(name, text=name, anchor=tk.CENTER)
            self.tree.column(name, anchor=tk.CENTER, width=size)

        self.tree.bind('<ButtonRelease-1>', self.remove_selection)

        self.tree.grid(row=0, column=0, sticky='nesw')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        for _ in range(50):
            self.add_pair('Paweł', 'Patryk', '2 - 0')
            self.add_pair('Piotr', 'Nicolas', '1 - 1')
            self.add_pair('Idol X', 'Idol Y', '2 - 0')

        self.config(padx=20, pady=20, bg='#efefef')

    def add_pair(self, white_name, black_name, points_str):
        self.tree.insert('', 'end', values=(len(self.tree.get_children()) + 1, white_name, black_name, points_str))

    def remove_selection(self, *args):
        print('Removing selection')
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)
