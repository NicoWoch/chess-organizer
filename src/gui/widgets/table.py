import random
import tkinter as tk
from collections import deque
from tkinter import font as tkfont
from typing import Any, Callable, Sequence

from src.gui.widgets.table_cell import TableCell

DEFAULT_TABLE_STYLE = {
    'name': None,
    'columns_count': 0,
    'header': None,
    'columns_weights': None,
    'header_height': 42,
    'row_height': 35,
    'header_bg': '#d5d5d5',
    'row_bg': '#f4f4f4',
    'odd_row_bg': None,
    'selected_bg': '#6ebcf4',
    'header_fg': 'black',
    'row_fg': 'black',
    'font': ('Arial', 14),
    'header_font': None,
    'gridlines': True,
    'gridlines_color': 'black',
    'gridlines_width': 1,
    'max_selection': float('inf'),
}


class Table(tk.Canvas):
    def __init__(self, parent, resize_listener: Callable[[], Any] = None, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(highlightthickness=0, borderwidth=0)

        self.style_name: Any = None
        self._style: dict[str, Any] = DEFAULT_TABLE_STYLE

        self._table: list[list[TableCell]] = []
        self._selected_indexes: deque[int] = deque()

        self.__redraw_event: Any = None
        self.__last_click: int | None = None
        self.__resize_listener = resize_listener

        self.bind('<Configure>', self._on_resize)
        self.bind('<Button-1>', self.__on_click)
        self.bind('<Shift-Button-1>', self.__on_click_shift)
        self.bind('<Control-a>', lambda e: self.__select_all_if_possble())
        self.bind('<Control-d>', lambda e: self.remove_selection())

    def change_table_style(self, style: dict[str, Any]):
        self._style = DEFAULT_TABLE_STYLE.copy()

        for key, value in style.items():
            if key not in self._style:
                raise KeyError(f'Unknown style key \'{key}\'')

            self._style[key] = value

        self.style_name = self._style['name']

        if self._style['header'] is not None:
            assert len(self._style['header']) == self._style['columns_count'], 'Header length is incorrect'

        if self._style['columns_weights'] is not None:
            assert len(self._style['columns_weights']) == self._style['columns_count'], \
                   'Columns weights length is incorrect'
        else:
            self._style['columns_weights'] = [1] * self._style['columns_count']

        if self._style['odd_row_bg'] is None:
            self._style['odd_row_bg'] = self._style['row_bg']

        if self._style['header_font'] is None:
            self._style['header_font'] = self._style['font']

        if not self._style['gridlines']:
            self._style['gridlines_width'] = 0

        self._style['font'] = self.__parse_font(self._style['font'])
        self._style['header_font'] = self.__parse_font(self._style['header_font'])
        self.__clear_table_fully()
        self.__create_header()
        self.__call_resize_listener()

    def __parse_font(self, font: Any):
        if font is None:
            return tkfont.Font(self, family='Arial', size=15)
        elif isinstance(font, (str, tuple)):
            return tkfont.Font(self, font=font)
        elif isinstance(font, tkfont.Font):
            return font
        else:
            raise ValueError(f'Bad font type \'{type(font)}\'')

    def __clear_table_fully(self):
        self.delete('all')
        self._table = []
        self._selected_indexes = deque()

    def __create_header(self):
        if self._style['header'] is not None:
            self._table.append([
                self.__create_cell_object(0, col, content).create(self)
                for col, content in enumerate(self._style['header'])
            ])

    def _on_resize(self, event: tk.Event):
        self.scale('all', 0, 0, event.width / self.winfo_reqwidth(), 1)
        self.config(width=event.width)

        if self.__redraw_event is not None:
            self.after_cancel(self.__redraw_event)

        self.__redraw_event = self.after(400, self.__resize_all_cells)

    def __resize_all_cells(self):
        for row in self._table:
            for cell in row:
                cell.update_size(self)

        self.__call_resize_listener()

    def __call_resize_listener(self):
        if self.__resize_listener is not None:
            self.__resize_listener()

    @property
    def columns_count(self) -> int:
        return self._style['columns_count']

    @property
    def rows_count(self) -> int:
        return len(self._table) - (1 if self._style['header'] is not None else 0)

    def update_table(self, table: Sequence[Sequence[Any]]):
        assert all(len(row) == self._style['columns_count'] for row in table), \
               'Length of some new rows does not match number of columns'

        self.remove_selection()

        if self._style['header'] is not None:
            table = [[], *table]

        for row, arr in enumerate(table[:len(self._table)]):
            self.__update_row(row, arr)

        for arr in table[len(self._table):]:
            self.__append_row(arr)

        while len(self._table) > len(table):
            self.__pop_row()

        self.__call_resize_listener()

    def __update_row(self, row_index: int, row: Sequence[Any]):
        for col, content in enumerate(row):
            new_cell = self.__create_cell_object(row_index, col, content)
            self._table[row_index][col] = self._table[row_index][col].update(self, new_cell)

    def __append_row(self, row: Sequence[Any]):
        self._table.append([
            self.__create_cell_object(len(self._table), col, content).create(self)
            for col, content in enumerate(row)
        ])

    def __pop_row(self):
        for cell in self._table.pop():
            cell.delete(self)

    def __create_cell_object(self, row: int, col: int, content: Any) -> TableCell:
        get_header: bool = self._style['header'] is not None and row == 0
        font = self._style['header_font'] if get_header else self._style['font']
        fg = self._style['header_fg'] if get_header else self._style['row_fg']
        bg = self._style['header_bg'] if get_header else self._style['row_bg']

        if (row + bool(self._style['header'] is not None)) % 2 == 0:
            bg = self._style['odd_row_bg']

        return TableCell(
            row=row, col=col,
            calculate_bbox=self._calculate_cell_bbox,
            is_row_selected=self._is_row_index_selected,
            content=content,
            font=font, fg=fg, bg=bg, selected_bg=self._style['selected_bg'],
            gridlines_width=self._style['gridlines_width'],
            gridlines_color=self._style['gridlines_color'],
        )

    def _calculate_cell_bbox(self, row: int, col: int) -> tuple[int, int, int, int]:
        start_x = 1
        full_width = self.winfo_width() - start_x - 3

        if self.winfo_width() <= 5:
            full_width = self.winfo_reqwidth() - start_x - 3

        column_unit = full_width / sum(self._style['columns_weights'])
        column_offset = int(sum(self._style['columns_weights'][:col]) * column_unit)
        column_size = int(self._style['columns_weights'][col] * column_unit)

        x, y = column_offset, row * self._style['row_height']
        width, height = column_size, self._style['row_height']

        if self._style['header'] is not None:
            if row == 0:
                height = self._style['header_height']
            else:
                y += self._style['header_height'] - self._style['row_height']

        return x + start_x, y, width, height

    def _is_row_index_selected(self, row_index: int) -> bool:
        return row_index in self._selected_indexes

    def __get_row_index(self, event: tk.Event) -> int | None:
        y = self.canvasy(event.y)

        if self._style['header'] is not None:
            row_index = (y - self._style['header_height']) // self._style['row_height'] + 1
        else:
            row_index = y // self._style['row_height']

        if row_index < 0 or row_index >= len(self._table) or (self._style['header'] is not None and row_index == 0):
            return

        return int(round(row_index))

    def __on_click(self, event: tk.Event):
        row_index = self.__get_row_index(event)

        if row_index is None:
            return

        self.__select_row_index(row_index, swap=True)
        self.__last_click = row_index

    def __on_click_shift(self, event: tk.Event):
        row_index = self.__get_row_index(event)

        if row_index is None:
            return

        if self.__last_click is not None:
            self.__select_row_index_itv(self.__last_click, row_index, swap=False)

        self.__last_click = row_index

    def __select_row_index(self, row_index: int, *, swap: bool = False):
        indexes_to_update = {row_index}

        if row_index in self._selected_indexes and swap:
            self._selected_indexes.remove(row_index)
        else:
            self._selected_indexes.append(row_index)

        while len(self._selected_indexes) > self._style['max_selection']:
            indexes_to_update |= {self._selected_indexes.popleft()}

        for index in indexes_to_update:
            for cell in self._table[index]:
                cell.update_selection(self)

    def __select_row_index_itv(self, start: int, end: int, *, swap: bool = False):
        if self._style['max_selection'] != float('inf'):
            return

        if end < start:
            start, end = end, start

        for row_index in range(start, end + 1):
            self.__select_row_index(row_index, swap=swap)

    def remove_selection(self):
        self._selected_indexes.clear()

        for row in self._table:
            for cell in row:
                cell.update_selection(self)

        self.__last_click = None

    def __select_all_if_possble(self):
        self.__select_row_index_itv(0, len(self._table) - 1)

    def get_selection(self) -> set[int]:
        offset = (0 if self._style['header'] is None else -1)
        return {
            index + offset
            for index in self._selected_indexes
        }

    def get_selection_with_rows(self) -> list[tuple[int, list[TableCell]]]:
        offset = (0 if self._style['header'] is None else -1)
        return [
            (index + offset, self._table[index])
            for index in self._selected_indexes
        ]

    def select_row(self, index: int):
        if index in self.get_selection():
            return

        row_index = (index if self._style['header'] is None else index + 1)
        self._selected_indexes.append(row_index)

        for cell in self._table[row_index]:
            cell.update_selection(self)

    def deselect_row(self, index: int):
        if index not in self.get_selection():
            return

        row_index = (index if self._style['header'] is None else index + 1)
        self._selected_indexes.remove(row_index)

        for cell in self._table[row_index]:
            cell.update_selection(self)

    def get_row_position(self, index: int) -> tuple[int, int]:
        row_index = (index if self._style['header'] is None else index + 1)
        _, y, _, height = self._calculate_cell_bbox(row_index, 0)
        return y, height


class ScrollableTableFrame(tk.Frame):
    def __init__(self, parent, scrollbar_width: int = 15, bottom_offset: int = 30):
        super().__init__(parent)

        self.configure(highlightthickness=0, borderwidth=0)

        self._scrollbar_width = scrollbar_width
        self._bottom_offset = bottom_offset
        self._scrollbar_state: bool = False

        self.configure(bg=parent['bg'])

        self.table = Table(self, resize_listener=self._on_table_resize)
        self._scrollbar = tk.Scrollbar(self, orient='vertical', command=self.table.yview)

        self.table.configure(yscrollcommand=self._scrollbar.set)
        self.table.yview('moveto', 0)

        self.table.place(relwidth=1, relheight=1)

    def _on_table_resize(self):
        if self.winfo_height() <= 5:
            return

        table_bbox = self.table.bbox('all') or (0, 0, 0, 0)
        self.table.configure(scrollregion=(0, 0, table_bbox[2], table_bbox[3] + self._bottom_offset))
        self._set_scrollbar_state(table_bbox[3] > self.winfo_height())

    def _set_scrollbar_state(self, state: bool):
        if self._scrollbar_state is state:
            return

        if state:
            self.table.place_forget()
            self.table.place(relwidth=1, width=-self._scrollbar_width, relheight=1)
            self._scrollbar.place(x=-self._scrollbar_width, relx=1, width=self._scrollbar_width, relheight=1)
        else:
            self.table.place_forget()
            self.table.place(relwidth=1, relheight=1)
            self._scrollbar.place_forget()

        self._scrollbar_state = state

    def scroll_to_row(self, index: int, hightlight: bool = False):
        y, row_height = self.table.get_row_position(index)
        max_y = sum(self.table.get_row_position(self.table.rows_count))

        y += row_height / 2
        y -= self.winfo_height() / 2

        self.table.yview_moveto(max(y, 0) / max_y)

        if hightlight:
            self.table.select_row(index)
            self.after(1000, lambda i=index: self.table.deselect_row(i))


def _test_window():
    app = tk.Tk()
    app.geometry('800x600')
    app.config(bg='green')

    main_frame = tk.Frame(app, bg='lightblue')
    main_frame.place(x=10, y=10, relwidth=1, relheight=1, width=-20, height=-20)

    scrollable_table = ScrollableTableFrame(main_frame)
    scrollable_table.place(relwidth=1, relheight=1)

    table = scrollable_table.table

    table.change_table_style({
        'columns_count': 3,
        'header': ['ala', 'ma', 'kota'],
        'columns_weights': [1, 2, 1],
        'max_selection': float('inf'),
    })

    btn = tk.Button(table, text='hello')

    table.update_table([
        ['a', 'b', 'c'],
        [1, 2, 3],
        [4.5, 5.2, 6.0],
        [btn, 1, 1],
        [tk.Button(table, text='1'), 1, 1],
        [tk.Button(table, text='2'), 1, 1],
        [tk.Button(table, text='3'), 1, 1],
        [tk.Button(table, text='4'), 1, 1],
        [tk.Button(table, text='5'), 1, 1],
    ])

    def random_matrix() -> list[list[Any]]:
        values_factories = [(lambda x=v: x) for v in [*'aeiouy', 'ala', 'ma', 'kota', 1, 2, 3.5]]
        btn_factories = [(lambda x=f: tk.Button(table, text=x())) for f in values_factories]
        return [
            [random.choice(values_factories * 2 + btn_factories)() for _ in range(3)]
            for _ in range(10)
        ]

    m = random_matrix()

    def swap():
        r1, r3 = [random.randrange(len(m)) for _ in range(2)]
        r2, r4 = [random.randrange(len(m[0])) for _ in range(2)]

        m[r1][r2], m[r3][r4] = m[r3][r4], m[r1][r2]

    def after():
        print('\nupdating table\n')
        table.update_table(m)

        for _ in range(random.randint(1, 10)):
            swap()

        app.after(5000, after)

    # app.after(3000, after)

    app.mainloop()


if __name__ == '__main__':
    _test_window()
