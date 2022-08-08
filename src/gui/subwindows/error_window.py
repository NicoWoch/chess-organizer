import tkinter as tk

from src.config import Config


class WindowException(Exception):
    pass


class ErrorWindow(tk.Toplevel):
    def __init__(self, parent, error_msg):
        super().__init__(parent)

        self.title('Błąd')
        self.geometry('+800+300')
        self.iconbitmap(Config.WINDOW_ICON_PATH)

        tk.Label(self, text=error_msg, foreground='red', font=('Times New Roman', 20, 'bold')) \
            .pack(fill='both', padx=10, pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    ErrorWindow(root, 'Błąd 303 w trakcie ....\ntutej -> "XxX"').mainloop()
