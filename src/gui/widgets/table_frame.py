import tkinter as tk


class TableFrame(tk.Frame):
    def __init__(self, parent, data=None, columns_weights=None, table_settings=None, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self._data = data if data is not None else []
        self._columns_weights = columns_weights if columns_weights is not None else []
        self._settings = table_settings if table_settings is not None else {}

        self.__set_defaults_for_settings()

        self._table = []
        self.__create_table()

    def __set_defaults_for_settings(self):
        self._settings.setdefault('gutter_x', 20)
        self._settings.setdefault('gutter_y', 5)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
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

        for x in range(len(self._table)):
            self.rowconfigure(x, weight=0 if unconfigure else 1)

        for y in range(len(self._table[0])):
            if y >= len(self._columns_weights):
                self._columns_weights.append(1)

            self.columnconfigure(y, weight=0 if unconfigure else self._columns_weights[y])

    def __remove_table(self):
        self.__configure_table(unconfigure=True)

        for x, row in enumerate(self._table):
            for y, _ in enumerate(row):
                self.__remove_cell(x, y)

        self._table = []

    def __update_table(self):
        table_rows = len(self._table)
        table_cols = len(self._table[0]) if len(self._table) > 0 else 0

        if table_rows != self.rows or table_cols != self.columns:
            self.__remove_table()
            self.__create_table()
            return

        for x in range(self.rows):
            for y in range(self.columns):
                self.__update_cell(x, y, self._data[x][y], self._table[x][y])

    @staticmethod
    def __is_value_a_widget_data(value) -> bool:
        return isinstance(value, tuple) and len(value) == 2 and issubclass(value[0], tk.Widget)

    def __create_cell(self, x: int, y: int):
        value = self._data[x][y]

        if self.__is_value_a_widget_data(value):
            widget = value[0](self, **value[1])
        else:
            widget = tk.Label(self, text=str(self._data[x][y]), bg=self.cget('bg'))
            widget.table_label = True

        widget.grid(row=x, column=y, sticky='nesw', ipadx=self._settings['gutter_x'], ipady=self._settings['gutter_y'])
        self._table[x][y] = widget

    def __remove_cell(self, x: int, y: int):
        self._table[x][y].grid_forget()
        self._table[x][y].destroy()
        self._table[x][y] = None

    def __update_cell(self, x: int, y: int, value, widget):
        if not self.__is_value_a_widget_data(value) and hasattr(widget, 'table_label'):
            text = widget.cget('text')

            if text == value:
                return

            widget.config(text=str(value))
            return

        self.__remove_cell(x, y)
        self.__create_cell(x, y)
