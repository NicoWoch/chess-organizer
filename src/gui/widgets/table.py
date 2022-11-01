import tkinter as tk
from tkinter import ttk


class Table(ttk.Treeview):
    def __init__(self, parent, style_prefix='default', style_theme=None):
        super().__init__(parent, show='headings')

        self.table_style = ttk.Style()
        self.table_style_name = f'{style_prefix}.Treeview'
        self['style'] = self.table_style_name

        if style_theme is not None:
            self.table_style.theme_use(style_theme)

        self['columns'] = ('x',)
        self.column_sizes = None

        self.bind('<Button-3>', self.remove_selection)
        self.bind('<Configure>', self._on_resize)
        self.configure_after = None

    def _on_resize(self, _):
        if self.configure_after is not None:
            self.after_cancel(self.configure_after)

        self.configure_after = self.after(100, self.update_columns)

    def style_headings(self, **kwargs):
        self.table_style.configure(f'{self.table_style_name}.Heading', **kwargs)

    def style_body(self, selected_fg='black', selected_bg='lightblue', **kwargs):
        self.table_style.configure(self.table_style_name, **kwargs)
        self.table_style.map(self.table_style_name,
                             foreground=[('selected', selected_fg)],
                             background=[('selected', selected_bg)])

    def style_even(self, **kwargs):
        self.tag_configure('even', **kwargs)

    def style_odd(self, **kwargs):
        self.tag_configure('odd', **kwargs)

    def update_columns(self):
        rows = [self.item(row)['values'] for row in self.get_children()]
        selected_rows = self.get_selected_ids()

        self.set_columns(self['columns'], self.column_sizes)

        for i, row in enumerate(rows):
            self.add_row(*row)

            if i in selected_rows:
                self.selection_add(self.get_children()[-1])

    def set_columns(self, names, sizes=None, _repeat=True):
        self.clear_rows()

        if sizes is None:
            sizes = [1 for _ in names]

        table_width = self.winfo_width()
        sizes_width = sum(sizes)
        size_factor = table_width / sizes_width

        self['columns'] = tuple(names)
        self.column_sizes = sizes
        for i, (name, size) in enumerate(zip(names, sizes)):
            if isinstance(size, int):
                minwidth, width = 20, int(size * size_factor)
            elif isinstance(size, tuple) and len(size) == 2:
                minwidth, width = (int(x * 2) for x in size)
            else:
                raise ValueError('Unknown size type')

            self.column(i, minwidth=minwidth, width=width, stretch=True, anchor=tk.CENTER)
            self.heading(i, text=name)

        self.update()
        if _repeat:
            self.set_columns(names, sizes, _repeat=False)

    def clear_rows(self):
        self.delete(*self.get_children())

    def add_row(self, *values):
        assert len(values) == len(self['columns']), 'Wrong amount of values in row'

        i = len(self.get_children())
        tag = 'even' if i % 2 == 0 else 'odd'

        self.insert('', 'end', values=(*values,), tags=(tag,))

    def get_selected_ids(self):
        selection = []
        for item in self.selection():
            selection.append(self.index(item))
        return selection

    def remove_selection(self, *_):
        for item in self.selection():
            self.selection_remove(item)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.update()

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.update()

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self.update()


if __name__ == '__main__':  # GUI Testing
    root = tk.Tk()
    root.geometry('600x300')

    t = Table(root, style_theme='clam')
    t.grid(sticky='nesw')

    t.style_headings(font='Arial 20')
    t.style_body(font='Arial 15')
    t.style_even(background='red')

    t.set_columns(['a', 'b', 'c'], [1, 3, 2])

    for _ in range(5):
        t.add_row('RA', 'RB', 'RC')

    def btn():
        t.set_columns(['a', 'b', 'c', 'd', 'e'])
        t.add_row(1, 1, 1, 2, 3)
        t.add_row(2, 3, 1, 4, 3)
        t.add_row(2, 3, 1, 5, 3)


    tk.Button(root, text='CLICK ME', command=btn).grid(row=2)

    root.columnconfigure(0, weight=1)
    root.mainloop()
