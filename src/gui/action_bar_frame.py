import tkinter as tk
import src.gui.gui_utils as utils


class ActionBarFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg='#8c5ccc')
        self.make_gui()

    def make_gui(self):
        utils.create_image_action_bar(self, [
            utils.Action('white_pawn.png', lambda: print('white'), tk.LEFT),
            utils.Action('black_pawn.png', lambda: print('black'), tk.LEFT),
            utils.Action('draw_icon.png', lambda: print('draw'), tk.LEFT),
            utils.Action('green_flag.png', lambda: print('green'), tk.LEFT),
            utils.Action('red_flag.png', lambda: print('red'), tk.LEFT),
            utils.Action('player.png', lambda: print('player'), tk.RIGHT),
            utils.Action('throphy.png', lambda: print('throphy'), tk.RIGHT),
        ], (50, 50), padx=20).grid(sticky='nesw')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
