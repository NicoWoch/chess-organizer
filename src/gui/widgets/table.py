import math
import random
import tkinter as tk
from tkinter import ttk
from typing import Union


ParsableLabel = Union[int, str, tk.Button]


class Table(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self._columns = []
        self._sizes = []
        self._sizes_sum = 0
        self._rows = []

        self._checkmarks = True
        self._selected_vars = []

        self.style = {
            'header': {
                'bg': '#ccc',
                'height': 30,
                'font': 'Arial 15',
                'padding': 5,
            },
            'row' : {
                'bg': {
                    'even': 'white',
                    'odd': '#eee',
                    'selected': 'lightblue',
                },
                'height': 25,
                'font': 'Arial 13',
                'selection_padding': 2,
            },
        }

        self.bind('<Button>', self.on_click)
        self.redraw()

    def on_click(self, event: tk.Event):
        widget_y = event.y_root - self.winfo_rooty()
        row_idx = math.floor((widget_y - self.style['header']['height'] - self.style['header']['padding']) / (self.style['row']['height']))

        if row_idx < 0 or row_idx >= len(self._rows):
            return

        var = self._selected_vars[row_idx]
        var.set(not var.get())

    def _col_pos_generator(self):
        checkmarks_size = 1 if self._checkmarks else 0

        now_pos = checkmarks_size / (self._sizes_sum + checkmarks_size)
        for col_size in self._sizes:
            col_percent_size = col_size / (self._sizes_sum + checkmarks_size)
            yield now_pos + col_percent_size / 2
            now_pos += col_percent_size

    def redraw(self):
        for elem in self.place_slaves():
            elem.destroy()

        if len(self._columns) == 0:
            return

        header_style = self.style['header']
        row_style = self.style['row']

        self.add_bindings(tk.Label(self, bg=header_style['bg'])) \
            .place(relwidth=1, height=header_style['height'] + header_style['padding'])

        for i, (col, col_pos) in enumerate(zip(self._columns, self._col_pos_generator())):
            self.parse_label(col, header_style['font'], header_style['bg']) \
                .place(relx=col_pos, y=2.5, height=header_style['height'], anchor='n')

        for i, row in enumerate(self._rows):
            y_pos = header_style['height'] + header_style['padding'] + (i * row_style['height'])
            bg_color = row_style['bg']['selected'] if self._selected_vars[i].get() else \
                       (row_style['bg']['odd'] if i % 2 == 0 else row_style['bg']['even'])

            self.add_bindings(tk.Label(self, bg=bg_color)) \
                .place(relwidth=1, y=y_pos - row_style['selection_padding'], height=row_style['height'] + row_style['selection_padding'] * 2)

            if self._checkmarks:
                self.add_bindings(tk.Checkbutton(self, variable=self._selected_vars[i], bg=bg_color)) \
                    .place(y=y_pos, height=row_style['height'], anchor='nw')

            for j, (item, col_pos) in enumerate(zip(row, self._col_pos_generator())):
                self.parse_label(item, row_style['font'], bg_color).place(relx=col_pos, y=y_pos, height=row_style['height'], anchor='n')

            self.rowconfigure(i, pad=2)

    def parse_label(self, lbl: ParsableLabel, font, bg):
        if isinstance(lbl, tk.Button):
            copy_attrs = {'text', 'command'}
            return tk.Button(self, {var: lbl[var] for var in copy_attrs})
        else:
            lbl = tk.Label(self, text=str(lbl), font=font, bg=bg)
            return self.add_bindings(lbl)

    def add_bindings(self, elem):
        elem.bind('<Button>', self.on_click)
        return elem

    def set_columns(self, columns: list[ParsableLabel], sizes: list[int] = None):
        if sizes is None:
            sizes = [1 for _ in columns]

        assert len(columns) == len(sizes)

        self._columns = columns
        self._sizes = sizes
        self._sizes_sum = sum(sizes)
        self._rows = []
        self._selected_vars = []

        self.redraw()

    def get_columns(self):
        return self._columns

    def add_row(self, *row: ParsableLabel):
        assert len(row) == len(self._columns)

        self._rows.append(row)
        self._selected_vars.append(tk.BooleanVar(value=False))
        self._selected_vars[-1].trace('w', lambda *_: self.redraw())

        self.redraw()

    def clear_rows(self):
        self._rows = []
        self._selected_vars = []
        self.redraw()

    def set_checkmarks_state(self, state: bool):
        self._checkmarks = state

    def get_selection(self):
        selection = []
        for i, item in enumerate(self._selected_vars):
            if item.get():
                selection.append(i)

        return selection

    def remove_selection(self, *_):
        for item in self._selected_vars:
            item.set(False)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x300')
    t = Table(root)
    t.place(relwidth=1, relheight=.5)

    t.set_columns(['a', 'b', 'c'], [1, 3, 2])
    vals = ['12736', 1231, ':)', 'DFsfSDF', 'BleBleBle', tk.Button(text='click here', command=lambda: print('It works!'))]
    for _ in range(5):
        random.shuffle(vals)
        t.add_row(*vals[:3])

    def btn():
        t.set_columns(['a', 'b', 'c', 'd', 'e'])
        t.add_row(1, 1, 1, 2, 3)
        t.add_row(2, 3, 1, 4, 3)
        t.add_row(2, 3, 1, 5, 3)


    tk.Button(root, text='CLICK ME', command=btn).place(relx=.5, rely=.5, anchor='n')

    root.mainloop()
