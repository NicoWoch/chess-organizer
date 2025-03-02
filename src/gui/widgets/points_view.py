import tkinter as tk
import tkinter.font as tkfont

from src.algorithms.constants import Points
from src.gui.utils import get_font_size_from_height


class PointsView(tk.Text):
    def __init__(self, parent, points: Points, row_height: int):
        super().__init__(parent)

        big_font_size = get_font_size_from_height(row_height, family='Arial')
        small_font_size = get_font_size_from_height(row_height - 8, family='Arial')

        self._big_font = tkfont.Font(self, family='Arial', size=big_font_size)
        self._small_font = tkfont.Font(self, family='Arial', size=small_font_size)

        self.tag_configure('big', font=self._big_font, justify='center')
        self.tag_configure('small', font=self._small_font, foreground='#222', justify='center')

        self.update_points(points)

        self.configure(state='disabled', borderwidth=0, cursor='arrow')
        self.configure(highlightthickness=0)
        self.bind('<<Selection>>', lambda e: self.selection_clear())

    def update_points(self, points: Points):
        self.delete('1.0', 'end')

        big_str = Points.points_with_halfs(points.big_points) + ', '
        small_strs = (Points.points_with_halfs(p) for p in points.small_points)

        self.insert('end', big_str, 'big')
        self.insert('end', ', '.join(small_strs), 'small')
