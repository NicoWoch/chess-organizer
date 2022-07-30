import os
import tkinter as tk
from collections import namedtuple
from typing import List

from PIL import Image, ImageTk

from src import db


PHOTOS = []


def create_image_btn(parent, img_filename: str, cmd=lambda: None, size=None):
    img_path = os.path.join(db.BASE_DIR, 'images', img_filename)

    if size is not None:
        img = Image.open(img_path).convert('RGBA')
        img = img.resize(size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
    else:
        photo = tk.PhotoImage(file=img_path)

    PHOTOS.append(photo)
    return tk.Button(parent, image=photo, command=cmd, borderwidth=0)


Action = namedtuple('Action', ('image_filename', 'cmd', 'side'))


def create_image_action_bar(parent, actions: List[Action], image_size, padx=0, pady=0):
    action_bar = tk.Frame(parent)

    for action in actions:
        create_image_btn(action_bar, action.image_filename, action.cmd, size=image_size)\
            .pack(side=action.side, padx=padx, pady=pady)

    return action_bar








