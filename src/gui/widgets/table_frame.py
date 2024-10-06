import tkinter as tk

from src.gui.widgets.resizing_font import ResizingFont
from src.gui.widgets.resizing_widgets import ResizingLabel

DEFAULT_SETTINGS = {
    'gutter_x': 10,
    'gutter_y': 10,
    'bg': None,
    'font': ('Comic Sans MS', 13),
    'has_header': True,
    'header_bg': '#522E1C',
    'header_font': ('Comic Sans MS', 16, 'bold'),
    'selectable': False,
    'selection_bg': '#89CFF0',
    'max_one_selection': False,
    'scroll': True,
}


class TableFrame(tk.Frame):
    def __init__(self, parent, data=None, columns_weights=None, table_settings=None, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self._data = data if data is not None else []
        self._columns_weights = columns_weights if columns_weights is not None else []
        self._settings: dict = DEFAULT_SETTINGS | (table_settings if table_settings is not None else {})

        self.container = self if not self._settings['scroll'] else self.__setup_scroll()

        if len(self._settings) > len(DEFAULT_SETTINGS):
            print(f'there are some wrong settings in: {self._settings}')

        self._table = []
        self._selection: set[int] = set()

        self.__create_table()

    def __setup_scroll(self):
        scrollbar = tk.Scrollbar(self, orient='vertical')

        canvas = tk.Canvas(self, bg=self.master.cget('bg'), bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=canvas.yview)

        container = tk.Frame(self)
        container_id = canvas.create_window(0, 0, window=container, anchor='nw')

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        def _configure_container(event):
            canvas.config(scrollregion=(0, 0, container.winfo_reqwidth(), container.winfo_reqheight()))

            if container.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=container.winfo_reqwidth())

        container.bind('<Configure>', _configure_container)

        def _configure_canvas(event):
            if container.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(container_id, width=canvas.winfo_width())

            if container.winfo_reqheight() > canvas.winfo_height():
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
            else:
                scrollbar.pack_forget()

        canvas.bind('<Configure>', _configure_canvas)

        return container

    def get_data(self):
        return [[value for value in row] for row in self._data]

    def set_data(self, data):
        self._data = data
        self.__update_table()

    @property
    def columns_weights(self):
        return self._columns_weights[:self.columns]

    @columns_weights.setter
    def columns_weights(self, weights):
        self._columns_weights = weights
        self.__configure_table()

    @property
    def rows(self):
        return len(self._data)

    @property
    def columns(self):
        if len(self._data) == 0:
            return 0

        return len(self._data[0])

    @property
    def _table_rows(self):
        return len(self._table)

    @property
    def _table_columns(self):
        if len(self._table) == 0:
            return 0

        return len(self._table[0])

    def __create_table(self):
        assert self._table == []

        self._table: list[list[tk.Widget | None]] = [[None] * self.columns for _ in range(self.rows)]

        self.__configure_table()

        for x in range(self.rows):
            for y in range(self.columns):
                self.__create_cell(x, y)

    def __configure_table(self, *, unconfigure=False):
        if len(self._table) == 0:
            return

        for y in range(self._table_columns):
            if y >= len(self._columns_weights):
                self._columns_weights.append(1)

            self.container.columnconfigure(y, weight=0 if unconfigure else self._columns_weights[y])

        self.__revalidate_selection()

    def __revalidate_selection(self):
        for item in tuple(self._selection):
            if item < 0 or item >= self.rows:
                self._selection.remove(item)

    def __remove_table(self):
        self.__configure_table(unconfigure=True)

        for x in range(self._table_rows):
            for y in range(self._table_columns):
                self.__remove_cell(x, y)

        self._table = []

    def __update_table(self):
        if self._table_rows != self.rows or self._table_columns != self.columns:
            self.__remove_table()
            self.__create_table()
            return

        for x in range(self.rows):
            for y in range(self.columns):
                self.__update_cell(x, y)

    def __create_cell(self, x: int, y: int):
        assert self._table[x][y] is None

        if isinstance(self._data[x][y], tk.Widget):
            self.__create_cell_from_widget(x, y, self._data[x][y])
        else:
            self.__create_cell_from_text(x, y, str(self._data[x][y]))

    def __create_cell_from_text(self, x: int, y: int, text: str):
        label = ResizingLabel(self.container, text=text, font=self.__get_row_font(x), bg=self.__get_row_bg(x))
        self.__update_font_size(label, x)
        setattr(label, '_table_label', True)
        self.__create_cell_from_widget(x, y, label)

    def __create_cell_from_widget(self, x: int, y: int, widget):
        self.__set_widget_background(x, widget)

        if self._settings['selectable'] and not isinstance(widget, tk.Button):
            func = lambda _, i=x: self.swap_selection(i)
            widget.bind('<Button-1>', func)

            if hasattr(widget, 'bind_click'):
                widget.bind_click(func)

        widget.grid(row=x, column=y, sticky='nesw', ipadx=self._settings['gutter_x'], ipady=self._settings['gutter_y'])
        self._table[x][y] = widget

    def __set_widget_background(self, x: int, widget):
        widget.config(bg=self.__get_row_bg(x))

        if hasattr(widget, 'set_background'):
            widget.set_background(self.__get_row_bg(x))

    def __remove_cell(self, x: int, y: int, *, destroy_widgets=True):
        self._table[x][y].grid_forget()

        if destroy_widgets or hasattr(self._table[x][y], '_table_label'):
            self._table[x][y].destroy()

        self._table[x][y] = None

    def __update_cell(self, x: int, y: int):
        if not isinstance(self._data[x][y], tk.Widget) and hasattr(self._table[x][y], '_table_label'):
            self.__update_text_cell(x, y)
        else:
            self.__update_widget_cell(x, y)

    def __update_text_cell(self, x: int, y: int):
        self._table[x][y].config(
            text=str(self._data[x][y]),
            bg=self.__get_row_bg(x)
        )
        self.__update_font_size(self._table[x][y], x)

    def __update_font_size(self, label: ResizingLabel, row: int):
        font_size = self.__get_row_font(row)[1]
        font = label.get_font()
        font.minsize = font_size - 5
        font.maxsize = font_size

    def __update_widget_cell(self, x: int, y: int):
        if hasattr(self._table[x][y], 'dynamic_swap'):
            success = self._table[x][y].dynamic_swap(self._data[x][y])

            if success:
                self.__set_widget_background(x, self._table[x][y])
                return

        self.__remove_cell(x, y, destroy_widgets=False)
        self.__create_cell(x, y)

    def __get_row_bg(self, row: int):
        if self._settings['selectable'] and row in self._selection:
            return self.__parse_transparent_color(self._settings['selection_bg'])

        if self._settings['has_header'] and row == 0:
            return self.__parse_transparent_color(self._settings['header_bg'])

        return self.__parse_transparent_color(self._settings['bg'])

    def __parse_transparent_color(self, color: str | None) -> str:
        return color if color is not None else self.cget('bg')

    def __get_row_font(self, row: int):
        if self._settings['has_header'] and row == 0:
            return self._settings['header_font']

        return self._settings['font']

    def swap_selection(self, row: int):
        if self._settings['has_header'] and row == 0:
            return

        if row in self._selection:
            self._selection.remove(row)
        elif self._settings['max_one_selection']:
            self._selection = {row}
        else:
            self._selection.add(row)

        self.__update_table()

    def get_selection(self) -> set[int]:
        return self._selection

    def clear_selection(self):
        self._selection.clear()
        self.__update_table()
