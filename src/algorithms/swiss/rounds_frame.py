import tkinter as tk


class RoundsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.labels = []

        self.columnconfigure(0, weight=1)

        self.add_round('Start')
        self.add_round('Round 1')
        self.add_round('Round 2')
        self.add_round('Round 3')

        self.config(bg='#bfbfbf', borderwidth=3, relief='groove')

    def add_round(self, text):
        label_id = len(self.labels)

        label = tk.Button(self, text=text, height=2, borderwidth=1, bg='white', command=lambda: self.change_round(label_id))
        label.grid(row=label_id, column=0, sticky='nesw')

        self.labels.append(label)

    def change_round(self, round_id):
        print(f'Changing round to {round_id}')
