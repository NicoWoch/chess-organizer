import tkinter as tk
from typing import Callable

from src.database import Database
from src.gui.subwindows.player_editor import PlayerEditor
from src.gui.widgets.table_frame import TableFrame
from src.tournament.player import Player


class PlayerExplorer(tk.Toplevel):
    def __init__(self, parent, database: Database, add_player: Callable[[Player], None]):
        super().__init__(parent)

        self.database = database
        self._add_player = add_player

        self.__define_layout()

    def __define_layout(self):
        self.title('Lista Wszystkich Graczy')
        self.geometry("700x800")
        self.maxsize(1200, 800)
        self.minsize(400, 180)

        self.table = TableFrame(self)
        self.__update_table(self.database.read())

        create_player_btn = tk.Button(self, text='Create\nplayer', command=self.__show_player_creation_window)

        self.table.place(x=0, y=0, relwidth=1, relheight=1)
        create_player_btn.place(x=-70, relx=1, y=-70, rely=1, width=60, height=60)

    def __update_table(self, db):
        headers = ['#', 'Gracz', 'Ranking', '', '', '']
        rows = [
            [
                i + 1,
                player.name,
                round(player.rating),
                self.__create_add_player_btn(i),
                self.__create_delete_player_btn(i),
                self.__create_edit_player_btn(i),
            ]
            for i, player in enumerate(db['players'])
        ]

        self.table.set_data([headers, *rows])

    def __create_add_player_btn(self, index: int):
        return tk.Button(self.table.container, text='OPEN', command=lambda i=index: self._add_player_to_tournament(i))

    def __create_delete_player_btn(self, index: int):
        return tk.Button(self.table.container, text='-', command=lambda i=index: self._delete_player(i))

    def __create_edit_player_btn(self, index: int):
        return tk.Button(self.table.container, text='EDIT', command=lambda i=index: self._show_player_editor(i))

    def _add_player_to_tournament(self, player_id: int):
        db = self.database.read()
        self._add_player(db['players'][player_id])

    def _delete_player(self, player_id: int):
        db = self.database.read()
        del db['players'][player_id]
        self.database.write(db)
        self.__update_table(db)

    def _show_player_editor(self, player_id: int):
        db = self.database.read()
        PlayerEditor(self, lambda p, i=player_id: self.__save_player_to_db(i, p), player_to_edit=db['players'][player_id])

    def __show_player_creation_window(self):
        PlayerEditor(self, self.__add_new_player_to_db)

    def __save_player_to_db(self, player_id: int, player: Player):
        db = self.database.read()
        db['players'][player_id] = player
        db['players'].sort()
        self.database.write(db)
        self.__update_table(db)

    def __add_new_player_to_db(self, player: Player):
        db = self.database.read()
        db['players'].append(player)
        db['players'].sort()
        self.database.write(db)
        self.__update_table(db)
