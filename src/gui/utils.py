import os
import tkinter as tk
from collections import namedtuple
from typing import Union

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


def create_image_action_bar(parent, actions: list[Action], image_size, padx=0, pady=0, tooltips=None):
    action_bar = tk.Frame(parent)
    frames: dict[str, tk.Frame] = {tk.LEFT: tk.Frame(action_bar), tk.CENTER: tk.Frame(action_bar), tk.RIGHT: tk.Frame(action_bar)}

    for i, action in enumerate(actions):
        button = create_image_btn(frames[action.side], action.image_filename, size=image_size, cmd=action.cmd)
        button.pack(side=tk.LEFT, padx=padx, pady=pady)

        if tooltips:
            ToolTip(button, text=tooltips[i])

    frames[tk.LEFT].pack(side=tk.LEFT)
    frames[tk.CENTER].place(relx=0.5, y=0, relheight=1, anchor=tk.N)
    frames[tk.RIGHT].pack(side=tk.RIGHT)

    return action_bar


class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)

        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

    def on_resize(self, event):
        wscale = event.width/self.width
        hscale = event.height/self.height
        self.width = event.width
        self.height = event.height

        self.scale("all", 0, 0, wscale, hscale)


class ToolTip:
    def __init__(self, widget, text=None):
        def make_tooltip():
            self.tooltip = tk.Toplevel()
            self.tooltip.overrideredirect(True)

            x = self.widget.winfo_rootx()
            y = self.widget.winfo_rooty() + self.widget.winfo_height()
            self.tooltip.geometry(f'+{x}+{y}')

            self.label = tk.Label(self.tooltip, text=self.text)
            self.label.pack()

        def on_enter(_):
            self._after_event = self.widget.after(500, lambda: make_tooltip())

        def on_leave(_):
            if self.tooltip is not None:
                self.tooltip.destroy()
                self.tooltip = None

            if self._after_event is not None:
                self.widget.after_cancel(self._after_event)
                self._after_event = None

        self.widget: tk.Frame = widget
        self.text = text
        self._after_event = None
        self.tooltip = None

        self.widget.bind('<Enter>', on_enter)
        self.widget.bind('<Leave>', on_leave)


class Rect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def center(self):
        return self.x1 + (self.width // 2), self.y1 + (self.height // 2)

    @property
    def n(self): return self.y1
    @property
    def e(self): return self.x2
    @property
    def s(self): return self.y2
    @property
    def w(self): return self.x1
    @property
    def nw(self): return self.w, self.n
    @property
    def ne(self): return self.e, self.n
    @property
    def sw(self): return self.w, self.s
    @property
    def se(self): return self.e, self.s

    def __str__(self):
        return f'Rect<{self.x1}, {self.y1}, {self.x2}, {self.y2}>'


def center_window(window: Union[tk.Tk, tk.Toplevel], size, offset=(0, 0)):
    top = (window.winfo_screenheight() - size[1]) // 2 + offset[1]
    left = (window.winfo_screenwidth() - size[0]) // 2 + offset[0]
    window.geometry('%dx%d+%d+%d' % (size[0], size[1], left, top))
