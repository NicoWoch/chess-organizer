import tkinter as tk

from src.gui.widgets.tkinter_image import TkinterImage


class ImageButton(tk.Button):
    def __init__(self, parent, filename: str, size: int | tuple[int, int], bg_parent=None, *args, **kwargs):
        if bg_parent is None:
            bg_parent = parent

        kwargs.setdefault('image', TkinterImage.open(filename, size))
        kwargs.setdefault('bg', bg_parent.cget('bg'))
        kwargs.setdefault('borderwidth', 0)
        kwargs.setdefault('width', kwargs['image'].size[0])
        kwargs.setdefault('height', kwargs['image'].size[1])

        super().__init__(parent, *args, **kwargs)
