import tkinter as tk

from src.config import Config


class WindowException(Exception):
    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg

    def __str__(self):
        return self.msg


class ErrorWindow(tk.Toplevel):
    def __init__(self, parent, error: WindowException):
        super().__init__(parent)

        self.title('Błąd')
        self.geometry('+750+500')
        self.iconbitmap(Config.WINDOW_ICON_PATH)
        self.resizable(False, False)

        tk.Label(self, text=error.msg, foreground='red', font=('Times New Roman', 20, 'bold')) \
            .pack(fill='both', padx=10, pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('0x0+0+0')
    ErrorWindow(root, WindowException('Błąd 303 w trakcie ....\ntutej -> "XxX"')).mainloop()
