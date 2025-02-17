import os
import tkinter as tk
from dataclasses import dataclass
from typing import Union, Callable, Optional

from PIL import Image, ImageTk

from src.config import Config

PHOTOS: dict[tuple[str, tuple[int, int]], tk.PhotoImage] = {}


def create_image(filename: str, size=None):
    if (filename, size) in PHOTOS:
        return PHOTOS[filename, size]

    full_path = os.path.join(Config.IMAGES_DIR, filename)

    if size is not None:
        img = Image.open(full_path).convert('RGBA')
        img = img.resize(size)
        photo = ImageTk.PhotoImage(img)
    else:
        photo = tk.PhotoImage(file=full_path)

    PHOTOS[filename, size] = photo
    return photo


def create_image_btn(parent, img_filename: str, size=None, cmd=lambda: None):
    photo = create_image(img_filename, size=size)

    return tk.Button(parent, image=photo, command=cmd, borderwidth=0)


@dataclass
class Action:
    image_filename: str
    cmd: Callable
    side: Union[tk.LEFT, tk.CENTER, tk.RIGHT]
    size: Optional[tuple[int, int]] = None


def create_image_action_bar(parent, actions: list[Action], image_size, padx=0, pady=0, tooltips=None):
    action_bar = tk.Frame(parent)
    frames: dict[str, tk.Frame] = {tk.LEFT: tk.Frame(action_bar), tk.CENTER: tk.Frame(action_bar), tk.RIGHT: tk.Frame(action_bar)}

    for i, action in enumerate(actions):
        size = action.size if action.size is not None else image_size
        button = create_image_btn(frames[action.side], action.image_filename, size=size, cmd=action.cmd)
        button.pack(side=tk.LEFT, padx=padx, pady=pady)

        if tooltips:
            tooltip_widget = ToolTip(button, text=tooltips[i])
            button.after(5_000, lambda: tooltip_widget)

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
        self.widget: tk.Frame = widget
        self.text = text
        self._create_event = None
        self.tooltip = None

        self.widget.bind('<Enter>', lambda _: self.__on_enter())
        self.widget.bind('<Leave>', lambda _: self.close())
        self.widget.bind('<Destroy>', lambda _: self.close())

    def create_tooltip(self):
        self.tooltip = tk.Toplevel()
        self.tooltip.overrideredirect(True)

        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tooltip.geometry(f'+{x}+{y}')

        label = tk.Label(self.tooltip, text=self.text)
        label.pack()

    def __on_enter(self):
        self._create_event = self.widget.after(1_000, self.create_tooltip)
        self.widget.after(10_000, self.close)

    def close(self):
        if self.tooltip is not None:
            self.tooltip.destroy()
            self.tooltip = None

        if self._create_event is not None:
            self.widget.after_cancel(self._create_event)
            self._create_event = None


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


def update_styles(source: dict, overrides: dict):
    for key, value in overrides.items():
        if isinstance(value, dict):
            update_styles(source[key], value)
        else:
            source[key] = overrides[key]


def add_icon(window: tk.Tk | tk.Toplevel):
    window.iconphoto(True, create_image(Config.WINDOW_ICON_PATH, (32, 32)))
