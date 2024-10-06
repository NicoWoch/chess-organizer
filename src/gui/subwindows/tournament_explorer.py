import tkinter as tk
from datetime import datetime, timedelta
from typing import Callable

from src.database import Database
from src.gui.widgets.table_frame import TableFrame
from src.gui.widgets.transient_toplevel import TransientToplevel


class TournamentExplorer(TransientToplevel):
    def __init__(self, parent, database: Database, open_tournament: Callable[[int], None]):
        super().__init__(parent)

        self.database = database
        self._open_tournament = open_tournament

        self.__define_layout()

    def __define_layout(self):
        self.title('Lista Wszystkich Turniejów')
        self.geometry("700x400")
        self.maxsize(1200, 800)
        self.minsize(570, 150)

        self.table = TableFrame(self, columns_weights=[1, 20, 3, 3, 1])
        self.__update_table()

        self.table.pack(fill=tk.BOTH)

    def __update_table(self):
        headers = ['#', 'Turniej', 'Data rozpoczęcia', 'Czas trwania', '']
        rows = [
            [
                i + 1,
                tournament.data.name,
                self.__parse_time(tournament.data.start_timestamp),
                self.__parse_time_difference(tournament.data.start_timestamp, tournament.data.finish_timestamp),
                self._create_open_btn(i),
            ]
            for i, tournament in enumerate(self.database.read()['tournaments'])
        ]

        self.table.set_data([headers, *rows])

    @staticmethod
    def __parse_time(time_: datetime, format_: str = '%d.%m   %H:%M') -> str:
        return time_.strftime(format_) if time_ is not None else '-'

    @staticmethod
    def __parse_time_difference(start: datetime, end: datetime) -> str:
        if start is None or end is None:
            return '-'

        delta = end - start
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60

        msg = []

        if delta.days > 0:
            msg.append(f'{delta.days} dni')

        if hours > 0:
            msg.append(f'{hours} godzin')

        if minutes > 0:
            msg.append(f'{minutes} minut')

        if len(msg) == 0:
            return '<1 minuta'

        return ', '.join(msg)

    def _create_open_btn(self, index: int):
        return tk.Button(self.table.container, text='open', command=lambda i=index: self.__open_btn_command(i))

    def __open_btn_command(self, index: int):
        self._open_tournament(index)
        self.destroy()
