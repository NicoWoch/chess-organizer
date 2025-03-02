import tkinter as tk
import tkinter.font as tkfont
from collections.abc import Callable

from src.gui import utils


class ConfirmWindow(tk.Toplevel):
    def __init__(self, parent, msg, on_confirm: Callable):
        super().__init__(parent)

        self.title('Potwierdź')
        utils.add_icon(self)
        self.resizable(False, False)

        self.on_confirm = on_confirm

        font = tkfont.Font(family='Calibri', size=18)
        question = f'Jesteś pewien że chcesz\n{msg} ?'

        window_width = self.__measure_text_width(question, font) + 30
        utils.center_window(self, (window_width, 110))

        label = tk.Label(self, text=question, font=font)
        label.place(x=0, y=0, relwidth=1)

        btn_yes = tk.Button(self, text='Tak', font=font, command=self._on_confirm)
        btn_no = tk.Button(self, text='Nie', font=font, command=self.destroy)

        btn_yes.place(x=0, rely=1, height=40, relwidth=.5, anchor=tk.SW)
        btn_no.place(relx=.5, rely=1, height=40, relwidth=.5, anchor=tk.SW)

    @classmethod
    def __measure_text_width(cls, text: str, font: tkfont.Font) -> int:
        return max(
            font.measure(line)
            for line in text.split('\n')
        )

    def _on_confirm(self):
        self.on_confirm()
        self.destroy()


def confirm(frame: tk.Misc, msg: str, on_confirm: Callable):
    ConfirmWindow(frame.winfo_toplevel(), msg, on_confirm).mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    confirm(root, 'usunąć gracza', lambda: print('CONFIRMED'))
