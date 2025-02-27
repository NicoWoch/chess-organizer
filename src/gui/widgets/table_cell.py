import tkinter as tk
from dataclasses import dataclass, field
from tkinter import font as tkfont
from typing import Any, Callable, Self


@dataclass(frozen=True)
class TableCell:
    row: int
    col: int
    content: Any

    calculate_bbox: Callable[[int, int], tuple[int, int, int, int]]
    is_row_selected: Callable[[int], bool]

    font: tkfont.Font
    fg: str
    bg: str
    selected_bg: str
    gridlines_width: int
    gridlines_color: str

    _creation_data: dict = field(init=False, compare=False, default_factory=lambda: {
        'is_created': False,
        'text_id': None, 'bg_id': None, 'win_id': None,
    })

    def _is_tkinter_object(self):
        return isinstance(self.content, (tk.Label, tk.Text, tk.Frame, tk.Button))

    def _is_text(self):
        return not self._is_tkinter_object()

    @property
    def _real_bg(self) -> str:
        return self.selected_bg if self.is_row_selected(self.row) else self.bg

    @property
    def _tkinter_elem_bbox(self) -> tuple[int, int, int, int]:
        margin_x, margin_y = 1, 1
        x, y, width, height = self.calculate_bbox(self.row, self.col)
        return x + margin_x, y + margin_y, width - 2 * margin_x + 1, height - 2 * margin_y + 1

    @property
    def _bg_pos(self) -> tuple[int, int, int, int]:
        x, y, width, height = self.calculate_bbox(self.row, self.col)
        return x, y, x + width + 1, y + height + 1

    @property
    def _text_pos(self) -> tuple[int, int]:
        x, y, width, height = self.calculate_bbox(self.row, self.col)
        return x + width // 2, y + height // 2

    def create(self, canvas: tk.Canvas) -> Self:
        assert not self._creation_data['is_created'], 'Table cell already created'

        self._creation_data['bg_id'] = canvas.create_rectangle(
            *self._bg_pos,
            fill=self._real_bg,
            width=self.gridlines_width,
            outline=self.gridlines_color
        )

        if self._is_tkinter_object():
            x, y, width, height = self._tkinter_elem_bbox

            win_id = canvas.create_window(x, y, width=width, height=height, anchor='nw', window=self.content)
            self.content.config(bg=self._real_bg)

            self._creation_data['win_id'] = win_id
            canvas.tag_lower(self._creation_data['bg_id'], self._creation_data['win_id'])
        else:
            self._creation_data['text_id'] = canvas.create_text(
                *self._text_pos,
                font=self.font, fill=self.fg,
                text=self.get_collapsed_text()
            )
            canvas.tag_lower(self._creation_data['bg_id'], self._creation_data['text_id'])

        self._creation_data['is_created'] = True
        return self

    def get_collapsed_text(self) -> str:
        if len(str(self.content)) <= 3:
            return str(self.content)

        x, y, width, height = self.calculate_bbox(self.row, self.col)
        text = str(self.content)

        while self.font.measure(text) > width:
            text = text[:-1]

        if text != str(self.content):
            text = text[:-3] + '...'

        return text

    def update_size(self, canvas: tk.Canvas):
        assert self._creation_data['is_created'], 'Table Cell not created'

        canvas.coords(self._creation_data['bg_id'], *self._bg_pos)

        if self._is_tkinter_object():
            x, y, width, height = self._tkinter_elem_bbox

            canvas.coords(self._creation_data['win_id'], x, y)
            canvas.itemconfigure(self._creation_data['win_id'], width=width, height=height)
        else:
            canvas.coords(self._creation_data['text_id'], *self._text_pos)
            canvas.itemconfigure(self._creation_data['text_id'], text=self.get_collapsed_text())

    def update_selection(self, canvas: tk.Canvas):
        assert self._creation_data['is_created'], 'Table cell has to be created first'

        canvas.itemconfigure(self._creation_data['bg_id'], fill=self._real_bg)

        if self._is_tkinter_object():
            self.content.config(bg=self._real_bg)

    def update(self, canvas: tk.Canvas, new_cell: Self) -> Self:
        assert self._creation_data['is_created'], 'Table cell has to be created first'
        assert not new_cell._creation_data['is_created'], 'New cell should not be created'

        if self == new_cell:
            return self

        if (cell := self.__update_two_texts(canvas, new_cell)) is not None:
            return cell

        self.delete(canvas)
        new_cell.create(canvas)

        return new_cell

    def __update_two_texts(self, canvas: tk.Canvas, new_cell: Self) -> Self | None:
        if not self._is_text() or not new_cell._is_text():
            return None

        canvas.itemconfigure(self._creation_data['bg_id'],
                             fill=new_cell._real_bg,
                             width=new_cell.gridlines_width,
                             outline=new_cell.gridlines_color)
        canvas.itemconfigure(self._creation_data['text_id'],
                             font=new_cell.font, fill=new_cell.fg,
                             text=new_cell.get_collapsed_text())

        new_cell._creation_data.update(self._creation_data)

        if (self.row, self.col) != (new_cell.row, new_cell.col):
            new_cell.update_size(canvas)

        return new_cell

    def delete(self, canvas: tk.Canvas):
        assert self._creation_data['is_created'], 'Table Cell not created'

        canvas.delete(self._creation_data['bg_id'])

        if self._is_tkinter_object():
            canvas.delete(self._creation_data['win_id'])
        else:
            canvas.delete(self._creation_data['text_id'])

        self._creation_data['is_created'] = False
