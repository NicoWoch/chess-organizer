import pprint
import sys
import tkinter as tk

from src.gui.widgets.transient_toplevel import TransientToplevel


class DeveloperConsole(TransientToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('700x600')

        self.parent = parent

        self.console = tk.Text(self, width=500, height=600, bg='#111111')
        self.console.place(x=0, y=0, relwidth=1, relheight=1, height=-40)

        self.input = tk.Entry(self, bg='#BFFFBF')
        self.input.place(x=0, rely=1, y=-40, relwidth=1, height=40)
        self.input.bind('<Return>', lambda _: self.__eval_command())
        self.input.bind('<Up>', lambda _: self.__prev_command())
        self.input.bind('<Down>', lambda _: self.__next_command())
        self.input.focus()

        self.command_history = []
        self.history_backward_ptr = 0

        clear_btn = tk.Button(self, text='CLEAR', command=self.clear_console)
        clear_btn.place(anchor='ne', relx=1, x=-8, y=8, width=70, height=50)

        self.__start_console()

    def __start_console(self):
        self.console.tag_config('info', foreground='white')
        self.console.tag_config('error', foreground='red')
        self.console.tag_config('eval', foreground='green')
        self.console.tag_config('eval_output', foreground='lightgreen')
        self.console.tag_config('unknown', foreground='blue')
        self.console.insert(tk.END, 'Developer Console Started\nPlease debug with patience :)\n', 'info')
        self.__capture_print_log()

    def clear_console(self):
        self.console.delete('1.0', tk.END)

    def __capture_print_log(self):
        print('Capturing Print Log...')
        self.old_print = print
        globals()['__builtins__']['print'] = self.__print_wrapper
        print('Print Log Captured')

    def __print_wrapper(self, *args, default_print_func=print, **kwargs):
        kwargs.setdefault('sep', ' ')
        kwargs.setdefault('end', '\n')

        if self.console.winfo_exists():
            file = kwargs.get('file', sys.stdout)

            if 'tag' in kwargs:
                tag = kwargs['tag']
            elif file is sys.stdout:
                tag = 'info'
            elif file is sys.stderr:
                tag = 'error'
            else:
                tag = 'unknown'

            self.console.insert(tk.END, kwargs['sep'].join(map(str, args)) + kwargs['end'], tag)
            self.console.see(tk.END)
        else:
            default_print_func('Released Print Log')
            globals()['__builtins__']['print'] = default_print_func

        kwargs.pop('tag', None)
        default_print_func(*args, **kwargs)

    def __eval_command(self):
        command = self.input.get()
        self.input.delete(0, tk.END)
        self.command_history.append(command)
        self.history_backward_ptr = 0

        self.__print_wrapper(f'Evaluating \'{command}\'', tag='eval')

        result = eval(command, self.__create_namespace())

        self.__print_wrapper(pprint.pformat(result), tag='eval_output')

    def __create_namespace(self) -> dict:
        namespace = {
            'app': self.parent,
            'tr': self.parent.tournament,
            'tr_id': self.parent.tournament_id,
            'db_controller': self.parent.database,
            'db': self.parent.database.read(),
            'dbp': self.parent.database.read().get('players', None),
            'dbt': self.parent.database.read().get('tournaments', None),
        }

        namespace['namespace'] = list(namespace.keys())

        help_str = f'Variables:\n\t' + '\n\t'.join(namespace['namespace'])
        namespace['help'] = type('helpobj', (), {'__repr__': lambda s: help_str})()

        namespace['clear'] = type('clearobj', (), {'__repr__': lambda s: (self.clear_console(), '')[1]})()

        return namespace

    def __prev_command(self):
        if self.history_backward_ptr == len(self.command_history):
            return

        self.history_backward_ptr += 1
        self.input.delete(0, tk.END)
        self.input.insert(0, self.command_history[-self.history_backward_ptr])

    def __next_command(self):
        if self.history_backward_ptr == 0:
            return

        self.history_backward_ptr -= 1
        self.input.delete(0, tk.END)

        if self.history_backward_ptr != 0:
            self.input.insert(0, self.command_history[-self.history_backward_ptr])
