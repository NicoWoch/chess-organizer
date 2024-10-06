import tkinter as tk

from src.gui.widgets.transient_toplevel import TransientToplevel


class DeveloperConsole(TransientToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('700x600')

        self.console = tk.Text(self, width=500, height=600)
        self.console.pack(fill=tk.BOTH)

        self.console.insert(tk.END, 'hello world\nthis is dev console\nplease debug with patience\n')
        self.__capture_print_log()

    def __capture_print_log(self):
        print('Capturing Print Log')
        self.old_print = print
        globals()['__builtins__']['print'] = self.__capturing_print

    def __capturing_print(self, *args, default_print_func=print, **kwargs):
        if self.console.winfo_exists():
            self.console.insert(tk.END, ' '.join(map(str, args)) + '\n')
        else:
            default_print_func('Released Print Log')
            globals()['__builtins__']['print'] = default_print_func

        default_print_func(*args, **kwargs)
