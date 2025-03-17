import tkinter as tk

from src.algorithms.constants import Points

BIG_POINTS_FONT = 'Arial', 12
SMALL_POINTS_FONT = 'Arial', 10


class PointsView(tk.Frame):
    def __init__(self, parent, points: Points):
        super().__init__(parent)

        big_str = Points.points_with_halfs(points.big_points)
        small_str = ', ' + ', '.join((Points.points_with_halfs(p) for p in points.small_points))

        self._big_label = tk.Label(self, text=big_str, font=BIG_POINTS_FONT)
        self._small_label = tk.Label(self, text=small_str, font=SMALL_POINTS_FONT)

        self.configure(bg=parent['bg'])

        self._big_label.place(relx=.5, rely=1, anchor='se')
        self._small_label.place(relx=.5, rely=1, anchor='sw')

    def configure(self, cnf: dict | None = None, **kwargs) -> dict | None:
        result = super().configure(cnf=cnf, **kwargs)

        background_changed = cnf is not None and ('bg' in cnf or 'background' in cnf)
        background_changed |= 'bg' in kwargs or 'background' in kwargs

        if background_changed:
            self._big_label.configure(bg=self['bg'])
            self._small_label.configure(bg=self['bg'])

        return result

    config = configure
