import tkinter as tk
from typing import Literal

from src.algorithms.constants import Points

POINTS_VIEW_STYLE = {
    'scoreboard': {
        'font': [('Arial', 13, 'bold'), ('Arial', 10)],
        'auto_align': [(120, 'left'), (float('inf'), 'leftcenter')],
    },
    'finish_table': {
        'font': [('Arial', 16, 'bold'), ('Arial', 13)],
        'auto_align': [(float('inf'), 'leftcenter')],
    },
}


class PointsView(tk.Frame):
    def __init__(self, parent, points: Points, style: dict):
        super().__init__(parent)

        big_str = Points.points_with_halfs(points.big_points)
        small_str = ', ' + ', '.join((Points.points_with_halfs(p) for p in points.small_points))

        self._style = style
        self._big_label = tk.Label(self, text=big_str, font=style['font'][0])
        self._small_label = tk.Label(self, text=small_str, font=style['font'][1])

        self.configure(bg=parent['bg'])

        self._auto_align_view()
        self.bind('<Configure>', lambda _: self._auto_align_view())

    def _auto_align_view(self):
        if self.winfo_width() <= 5:
            return

        for treshold, align in self._style['auto_align']:
            if self.winfo_width() <= treshold:
                self._align_view(align)
                return

    def _align_view(self, position: Literal['left', 'leftcenter']):
        if position == 'leftcenter':
            self._big_label.place(x=-20, relx=.5, y=0, rely=1, anchor='se', relheight=1)
            self._small_label.place(x=-20, relx=.5, y=0, rely=1, anchor='sw', relheight=1)
        elif position == 'left':
            self._big_label.place(x=34, relx=0, y=0, rely=1, anchor='se', relheight=1)
            self._small_label.place(x=34, relx=0, y=0, rely=1, anchor='sw', relheight=1)

    def configure(self, cnf: dict | None = None, **kwargs) -> dict | None:
        result = super().configure(cnf=cnf, **kwargs)

        background_changed = cnf is not None and ('bg' in cnf or 'background' in cnf)
        background_changed |= 'bg' in kwargs or 'background' in kwargs

        if background_changed:
            self._big_label.configure(bg=self['bg'])
            self._small_label.configure(bg=self['bg'])

        return result

    config = configure
