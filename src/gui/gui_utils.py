import os
import tkinter as tk
import tkinter.ttk as ttk
from collections import namedtuple
from typing import List

from PIL import Image, ImageTk

from src.config import Config

PHOTOS = []


def create_image(img_filename: str, size=None):
    img_path = os.path.join(Config.GUI_IMAGES_DIR, img_filename)

    if size is not None:
        img = Image.open(img_path).convert('RGBA')
        img = img.resize(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
    else:
        photo = tk.PhotoImage(file=img_path)

    PHOTOS.append(photo)
    return photo


def create_image_btn(parent, img_filename: str, size=None, cmd=lambda: None):
    photo = create_image(img_filename, size=size)

    return tk.Button(parent, image=photo, command=cmd, borderwidth=0)


Action = namedtuple('Action', ('image_filename', 'cmd', 'side'))


def create_image_action_bar(parent, actions: List[Action], image_size, padx=0, pady=0):
    action_bar = tk.Frame(parent)

    for action in actions:
        create_image_btn(action_bar, action.image_filename, size=image_size, cmd=action.cmd)\
            .pack(side=action.side, padx=padx, pady=pady)

    return action_bar


class Table(ttk.Treeview):
    def __init__(self, parent, style_prefix='default', style_theme=None):
        super().__init__(parent, show='headings')

        self.table_style = ttk.Style()
        self.table_style_name = f'{style_prefix}.Treeview'
        self['style'] = self.table_style_name

        if style_theme is not None:
            self.table_style.theme_use(style_theme)

        self['columns'] = ('x',)

        self.bind('<Button-3>', self.remove_selection)

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

    def set_columns(self, names, sizes=None):
        self.clear_rows()

        if sizes is None:
            sizes = [1 for _ in names]

        table_width = self.winfo_width()
        sizes_width = sum(sizes)
        size_factor = table_width / sizes_width

        self['columns'] = tuple(names)
        for i, (name, size) in enumerate(zip(names, sizes)):
            if isinstance(size, int):
                minwidth, width = 20, int(size * size_factor)
            elif isinstance(size, tuple) and len(size) == 2:
                minwidth, width = (int(x * 2) for x in size)
            else:
                raise ValueError('Unknown size type')

            self.column(i, minwidth=minwidth, width=width, stretch=True, anchor=tk.CENTER)
            self.heading(i, text=name)

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
