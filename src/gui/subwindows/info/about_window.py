import tkinter as tk
from src.gui import utils

ABOUT_TEXT = '''Program do zarządzania
turniejami szachowymi
z algorytmem swiss


Autor:     Nicolas Wochnik

Testerzy:  Magdalena Gandyk
     Piotr Wolter'''


class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title('O programie')
        utils.add_icon(self)
        utils.center_window(self, (400, 225))
        self.resizable(False, False)

        logo_image = utils.create_image('logo.png', size=(100, 100))
        logo_label = tk.Label(self, image=logo_image)
        logo_label.grid(row=0, column=0)

        about_label = tk.Label(self, text=ABOUT_TEXT, font=('Arial', 12))
        about_label.grid(row=0, column=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    AboutWindow(root).mainloop()
