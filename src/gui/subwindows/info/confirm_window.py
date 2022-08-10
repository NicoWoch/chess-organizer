import tkinter as tk
from collections.abc import Callable

import src.gui.gui_utils as utils
from src.config import Config


class ConfirmWindow(tk.Toplevel):
    def __init__(self, parent, msg, on_confirm: Callable):
        super().__init__(parent)

        self.title('Potwierdź')
        self.iconbitmap(Config.WINDOW_ICON_PATH)

        if len(msg) < 28:
            utils.center_window(self, (300, 110))
        else:
            utils.center_window(self, (420, 110))

        self.on_confirm = on_confirm

        label = tk.Label(self, text=f'Jesteś pewien że chcesz\n{msg} ?', font=('Calibri', 18))
        label.place(x=0, y=0, relwidth=1)

        btn_yes = tk.Button(self, text='Tak', font=('Calibri', 18), command=self._on_confirm)
        btn_no = tk.Button(self, text='Nie', font=('Calibri', 18), command=self.destroy)

        btn_yes.place(x=0, rely=1, height=40, relwidth=.5, anchor=tk.SW)
        btn_no.place(relx=.5, rely=1, height=40, relwidth=.5, anchor=tk.SW)

    def _on_confirm(self):
        self.on_confirm()
        self.destroy()


def confirm(frame: tk.Misc, msg: str, on_confirm: Callable):
    ConfirmWindow(frame.winfo_toplevel(), msg, on_confirm).mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    confirm(root, 'usunąć gracza', lambda: print('CONFIRMED'))
