import tkinter as tk
from gui.rounds_frame import RoundsFrame
from gui.pairs_frame import PairsFrame
from gui.functions_frame import FunctionsFrame


WINDOW_NAME = 'Chess Organizer V0.1'
WINDOW_ICON_PATH = 'images/icon.ico'
WINDOW_SIZE = 1080, 640


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_NAME)
        self.iconbitmap(WINDOW_ICON_PATH)
        self.geometry('%dx%d+%d+%d' % (WINDOW_SIZE[0], WINDOW_SIZE[1],
                                       (self.winfo_screenwidth() - WINDOW_SIZE[0]) / 2,
                                       (self.winfo_screenheight() - WINDOW_SIZE[1]) / 2))

        self.functions_widget = FunctionsFrame(self)
        self.functions_widget.grid(row=0, column=0, columnspan=2, sticky='nesw')

        self.rounds_widget = RoundsFrame(self)
        self.rounds_widget.grid(row=1, column=0, sticky='nesw')

        self.pairs_widget = PairsFrame(self)
        self.pairs_widget.grid(row=1, column=1, sticky='nesw')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)



if __name__ == '__main__':
    App().mainloop()
